package main

import (
	"bufio"
	"bytes"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"

	humanize "github.com/dustin/go-humanize"
	"github.com/google/shlex"
)

func containsDotDot(v string) bool {
	if !strings.Contains(v, "..") {
		return false
	}
	for _, ent := range strings.FieldsFunc(v, isSlashRune) {
		if ent == ".." {
			return true
		}
	}
	return false
}

func isSlashRune(r rune) bool { return r == '/' || r == '\\' }

func isDirNested(parent, child string) error {
	abs, err := filepath.Abs(child)
	if err != nil {
		panic(fmt.Sprintf("could not resolve path: %v", err))
	}

	diff, err := filepath.Rel(parent, abs)
	if err != nil {
		return fmt.Errorf("could not determine relative path: %v", err)
	}

	if containsDotDot(diff) {
		return fmt.Errorf("cannot use paths outside current working directory")
	}

	return nil
}

func resolvePathSafe(slashPath string) (string, error) {
	relPath := filepath.FromSlash(slashPath)

	cwd, err := os.Getwd()
	if err != nil {
		panic(fmt.Sprintf("could not determine current working directory: %v", err))
	}

	if err := isDirNested(cwd, relPath); err != nil {
		return "", err
	}

	return relPath, nil
}

func readFile(relPath string) ([]byte, error) {
	data, err := os.ReadFile(relPath)
	if err != nil {
		return nil, fmt.Errorf("error reading file %q: %v", relPath, err)
	}
	return data, nil
}

func writeFile(slashPath, data string) error {
	relPath, err := resolvePathSafe(slashPath)
	if err != nil {
		return err
	}
	err = os.WriteFile(relPath, []byte(data), 0660)
	if err != nil {
		return fmt.Errorf("error writing file %q: %v", relPath, err)
	}
	return nil
}

func downloadFile(url, slashPath string) (string, error) {
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return "", fmt.Errorf("error creating HTTP request: %v", err)
	}

	baseName := path.Base(req.URL.Path)
	if baseName == "/" {
		baseName = ""
	}

	destIsDir := slashPath == "" || strings.HasSuffix(slashPath, "/")

	relPath, err := resolvePathSafe(slashPath)
	if err != nil {
		return "", fmt.Errorf("error resolving file path %q: %v", slashPath, err)
	}

	if destIsDir {
		if baseName == "" {
			// TODO inspect Content-Disposition instead of bailing out?
			return "", fmt.Errorf("could not determine file name from url %q", url)
		}
		relPath = filepath.Join(relPath, baseName)
	}

	if _, err := os.Stat(relPath); err == nil {
		// XXX prompt for rename
		fmt.Printf("Download skipped: %q\n", relPath)
		return relPath, nil
	}

	relPathDir := filepath.Dir(relPath)
	if relPathDir != "." && relPathDir != "/" {
		if err := os.MkdirAll(relPathDir, 0750); err != nil {
			return "", fmt.Errorf("error creating desination directory %q: %v", relPathDir, err)
		}
	}

	out, err := os.Create(relPath)
	if err != nil {
		return "", fmt.Errorf("error creating file %q: %v", relPath, err)
	}
	defer out.Close()

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		return "", fmt.Errorf("error making HTTP request: %v", err)
	}
	defer res.Body.Close()

	n, err := io.Copy(out, res.Body)
	if err != nil {
		return "", fmt.Errorf("error writing file %q: %v", relPath, err)
	}

	fmt.Printf("Downloaded %s: %s\n", relPath, humanize.Bytes(uint64(n)))

	return relPath, nil
}

var (
	headerRegex      = regexp.MustCompile(`(?s)#\s*-{3,}\s*\n(.+?)\n\s*#\s*-{3,}\s*`)
	commentRegex     = regexp.MustCompile(`^\s*#\s?`)
	errNoHeaderFound = errors.New("no header found")
	errUnexpectedEOF = errors.New("unexpected end of file reading header")
)

type Command struct {
	t    string
	args []string
}

func parseHeader(code []byte) ([]Command, error) {
	match := headerRegex.FindSubmatch(code)
	if len(match) < 2 {
		return nil, errNoHeaderFound
	}

	var commands []Command
	buffering := false
	scanner := bufio.NewScanner(bytes.NewReader(match[1]))
	for scanner.Scan() {
		line := string(commentRegex.ReplaceAll(scanner.Bytes(), nil))
		tokens, err := shlex.Split(line)
		if err != nil {
			return nil, fmt.Errorf("error parsing line: %v", err)
		}
		if len(tokens) == 0 {
			continue
		}
		cmd, args := strings.ToUpper(tokens[0]), tokens[1:]
		if cmd == "FILE" {
			if len(args) != 2 {
				return nil, fmt.Errorf("FILE: want %q, got %q", "FILE target-path eof-marker", line)
			}
			var buffer []string
			buffering = true
			eofMarker := args[1]
			for buffering && scanner.Scan() {
				line := string(commentRegex.ReplaceAll(scanner.Bytes(), nil))
				if strings.TrimSpace(line) == eofMarker {
					line = ""
					buffering = false
					break
				}
				buffer = append(buffer, line)
			}
			args[1] = strings.Join(buffer, "\n")
		}
		commands = append(commands, Command{cmd, args})
	}
	if buffering {
		return nil, errUnexpectedEOF
	}
	return commands, nil
}

var (
	pythonCandidates        = []string{"python3", "python"}
	pythonWindowsCandidates = []string{"py", "python3", "python"}
)

func findPythonExecutable() (string, error) {
	candidates := pythonCandidates
	if runtime.GOOS == "windows" {
		candidates = pythonWindowsCandidates
	}
	for _, name := range candidates {
		p, err := exec.LookPath(name)
		if err == nil {
			return p, nil
		}
	}
	return "", fmt.Errorf("python executable not found (tried %v)", pythonCandidates)
}

func newPythonEnv(vars []string) (*Env, error) {
	exe, err := findPythonExecutable()
	if err != nil {
		return nil, err
	}

	// Run python -m venv venv
	if err := execCommand(exe, []string{"-m", "venv", "venv"}, nil); err != nil {
		return nil, fmt.Errorf("error initializing virtual environment: %v", err)
	}

	// Use sandboxed python for future commands
	var vexe string
	if runtime.GOOS == "windows" {
		// .\venv\Scripts\python.exe
		vexe = filepath.Join("venv", "Scripts", "python.exe")
	} else {
		// ./venv/bin/python
		vexe = filepath.Join("venv", "bin", "python")
	}

	return &Env{vars, func(name string) string {
		if name == "python" {
			return vexe
		}
		return name
	}}, nil
}

type Env struct {
	vars      []string
	translate func(string) string
}

func newEnv(file string) (*Env, error) {
	vars := os.Environ()
	lang := filepath.Ext(file)
	switch lang {
	case ".py":
		return newPythonEnv(vars)
	}
	return nil, fmt.Errorf("unsupported file type %q", lang)
}

func (env *Env) Set(name, value string) {
	env.vars = append(env.vars, name+"="+value)
}

func execCommand(name string, args, env []string) error {
	cmd := exec.Command(name, args...)
	cmd.Env = env

	output, err := cmd.CombinedOutput()
	fmt.Println(string(output)) // TODO only show if error or verbose
	if err != nil {
		return fmt.Errorf("error executing %q %v: %v", name, args, err)
	}
	return nil
}

func startCommand(name string, args, env []string) error {
	cmd := exec.Command(name, args...)
	cmd.Env = env
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		return fmt.Errorf("error executing %q %v: %v", name, args, err)
	}
	return nil
}

func interpret(env *Env, commands []Command) error {
	for _, command := range commands {
		args := command.args
		switch command.t {
		case "ENV":
			if len(args) != 2 {
				return fmt.Errorf("ENV failed: want %q, got %#v", "ENV name value", args)
			}
			name, value := args[0], args[1]
			env.Set(name, value)
		case "GET":
			var url, localPath string
			if len(args) == 1 {
				url = args[0]
			} else if len(args) == 2 {
				url, localPath = args[0], args[1]
			} else {
				return fmt.Errorf("GET failed: want %q, got %#v", "GET remote-url [local-path]", args)
			}
			if _, err := downloadFile(url, localPath); err != nil {
				return fmt.Errorf("GET failed: %v", err)
			}
		case "FILE":
			localPath, contents := args[0], args[1]
			if err := writeFile(localPath, contents); err != nil {
				return fmt.Errorf("FILE failed: %v", err)
			}
		case "RUN":
			name, args := args[0], args[1:]
			if err := execCommand(env.translate(name), args, env.vars); err != nil {
				return fmt.Errorf("RUN failed: %v", err)
			}
		case "START":
			name, args := args[0], args[1:]
			if err := startCommand(env.translate(name), args, env.vars); err != nil {
				return fmt.Errorf("START failed: %v", err)
			}
		}
	}

	return nil
}

func run(url string) error {
	mainFilePath, err := downloadFile(url, "")
	if err != nil {
		return fmt.Errorf("error downloading main file: %v", err)
	}

	code, err := readFile(mainFilePath)
	if err != nil {
		return fmt.Errorf("error reading main file: %v", err)
	}

	commands, err := parseHeader(code)
	if err != nil {
		return fmt.Errorf("error parsing header: %v", err)
	}

	env, err := newEnv(mainFilePath)
	if err != nil {
		return fmt.Errorf("error initializing environment: %v", err)
	}

	if err := interpret(env, commands); err != nil {
		return err
	}

	return nil
}

func main() {
	url := "https://gist.githubusercontent.com/lo5/d982e34b7684d4a1135d2bb7c06e6b99/raw/7251fdd3a2f283cfaa66a0c9c5768a374bb1a0ee/app.py"
	if err := run(url); err != nil {
		fmt.Println(err)
	}
}
