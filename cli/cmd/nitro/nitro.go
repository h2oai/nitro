package main

import (
	"bufio"
	"bytes"
	"context"
	"errors"
	"flag"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"os/exec"
	"path"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"

	humanize "github.com/dustin/go-humanize"
	"github.com/google/shlex"
	"github.com/peterbourgon/ff/v3/ffcli"
	"gopkg.in/yaml.v3"
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

func showFile(slashPath string) error {
	relPath, err := resolvePathSafe(slashPath)
	if err != nil {
		return err
	}
	file, err := os.Open(relPath)
	if err != nil {
		return fmt.Errorf("error reading file %q: %v", relPath, err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	n := 0
	for scanner.Scan() {
		n++
		if n > 256 { // Roughly four pages on a HD-sized terminal.
			fmt.Println("--- truncated ---")
			break
		}
		fmt.Println(scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		return fmt.Errorf("error scanning file %q: %v", relPath, err)
	}
	return nil
}

func downloadFile(urlPath, slashPath string) (string, error) {
	fmt.Printf("Downloading %s\n", urlPath)

	req, err := http.NewRequest("GET", urlPath, nil)
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
			return "", fmt.Errorf("could not determine file name from url %q", urlPath)
		}
		relPath = filepath.Join(relPath, baseName)
	}

	if _, err := os.Stat(relPath); err == nil {
		fmt.Printf("Download skipped: %q already exists.\n", relPath)
		return relPath, nil
	}

	relPathDir := filepath.Dir(relPath)
	if relPathDir != "." && relPathDir != "/" {
		if err := os.MkdirAll(relPathDir, 0750); err != nil {
			return "", fmt.Errorf("error creating destination directory %q: %v", relPathDir, err)
		}
	}

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		return "", fmt.Errorf("error making HTTP request: %v", err)
	}
	defer res.Body.Close()

	out, err := os.Create(relPath)
	if err != nil {
		return "", fmt.Errorf("error creating file %q: %v", relPath, err)
	}
	defer out.Close()

	n, err := io.Copy(out, res.Body)
	if err != nil {
		return "", fmt.Errorf("error writing file %q: %v", relPath, err)
	}

	fmt.Printf("Downloaded %s: %s\n", relPath, humanize.Bytes(uint64(n)))

	return relPath, nil
}

var (
	commentRegex            = regexp.MustCompile(`^\s*#\s?`)
	breakRegex              = regexp.MustCompile(`\\\s*$`)
	headerRegex             = regexp.MustCompile(`^\s*#\s*={3,}\s*$`)
	setupRegex              = regexp.MustCompile(`(?i)^\s*SETUP\s*:\s*$`)
	pythonCandidates        = []string{"python3", "python"}
	pythonWindowsCandidates = []string{"py", "python3", "python"}
	errNoHeaderFound        = errors.New("no header found")
	errUnexpectedEOF        = errors.New("unexpected end of file reading header")
	nl                      = []byte{'\n'}
)

type Header struct {
	meta     map[string]interface{}
	commands []Command
}

type Command struct {
	t    string
	args []string
}

type Line struct {
	text []byte
	n    int // line number
}

func parseHeader(code []byte) (Header, error) {
	var (
		header Header
		yml    [][]byte
		script []Line
	)

	inHeader, inSetup := false, false
	n := 0
	scanner := bufio.NewScanner(bytes.NewReader(code))
	for scanner.Scan() {
		n++
		text := scanner.Bytes()
		if headerRegex.Match(text) {
			if inHeader {
				break
			}
			inHeader = true
			continue
		}
		if !inHeader {
			continue
		}
		if !commentRegex.Match(text) {
			if len(bytes.TrimSpace(text)) == 0 { // empty lines OK
				continue
			}
			return header, errUnexpectedEOF
		}

		text = commentRegex.ReplaceAll(text, nil)

		if setupRegex.Match(text) {
			if inSetup {
				return header, fmt.Errorf("unexpected %q in header on line %d", text, n)
			}
			inSetup = true
			continue
		}

		if inSetup {
			script = append(script, Line{text, n})
		} else {
			yml = append(yml, text)
		}
	}

	script = joinBrokenLines(script)

	meta := make(map[string]interface{})
	if err := yaml.Unmarshal(bytes.Join(yml, nl), meta); err != nil {
		return header, fmt.Errorf("error parsing header YAML: %v", err)
	}

	commands, err := parseCommands(script)
	if err != nil {
		return header, err
	}

	header.meta = meta
	header.commands = commands

	return header, nil

}

func joinBrokenLines(lines []Line) []Line {
	var joined []Line
	join := false
	for i, line := range lines {
		if join && i > 0 {
			lines[i-1].text = append(lines[i-1].text, breakRegex.ReplaceAll(line.text, nil)...)
		} else {
			joined = append(joined, line)
		}
		join = breakRegex.Match(line.text)
	}
	return joined
}

func parseCommands(lines []Line) ([]Command, error) {
	var (
		commands  []Command
		buffer    []string
		eofMarker string
	)

	for _, line := range lines {
		if eofMarker == "" {
			tokens, err := shlex.Split(string(line.text))
			if err != nil {
				return nil, fmt.Errorf("error parsing line: %v", err)
			}
			if len(tokens) == 0 {
				continue
			}
			cmd, args := strings.ToUpper(tokens[0]), tokens[1:]
			if cmd == "FILE" {
				if len(args) != 2 {
					return nil, fmt.Errorf("FILE: want %q, got %q", "FILE target-path eof-marker", line.text)
				}
				eofMarker = args[1]
			}
			commands = append(commands, Command{cmd, args})
		} else {
			text := string(line.text)
			if strings.TrimSpace(text) == eofMarker {
				text = ""
				cmd := commands[len(commands)-1]
				cmd.args[1] = strings.Join(append(buffer, ""), "\n")
				commands[len(commands)-1] = cmd
				buffer = nil
				eofMarker = ""
			} else {
				buffer = append(buffer, text)
			}
		}
	}
	if eofMarker != "" {
		return nil, errUnexpectedEOF
	}
	return commands, nil
}

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

func newPythonEnv(conf *Conf, vars []string) (*Env, error) {
	if conf.python == "" {
		python, err := findPythonExecutable()
		if err != nil {
			return nil, err
		}
		conf.python = python
	}

	if _, err := os.Stat("venv"); err == nil {
		fmt.Println("Virtual environment already available.")
	} else {
		fmt.Printf("Creating virtual environment using %q...\n", conf.python)
		// Run python -m venv venv
		if err := execCommand(conf.python, []string{"-m", "venv", "venv"}, nil, conf.verbose); err != nil {
			return nil, fmt.Errorf("error initializing virtual environment: %v", err)
		}
	}

	// Use sandboxed python from this point on.
	var vexe string
	if runtime.GOOS == "windows" {
		// .\venv\Scripts\python.exe
		vexe = filepath.Join("venv", "Scripts", "python.exe")
	} else {
		// ./venv/bin/python
		vexe = filepath.Join("venv", "bin", "python")
	}

	if _, err := os.Stat(vexe); err == nil {
		fmt.Printf("Found %q\n", vexe)
	} else {
		return nil, fmt.Errorf("could not find Python executable at %q", vexe)
	}

	fmt.Println("Bootstrapping pip...")
	if err := execCommand(vexe, []string{"-m", "ensurepip", "--upgrade"}, nil, conf.verbose); err != nil {
		return nil, fmt.Errorf("error bootstrapping pip: %v", err)
	}

	return &Env{
		vars: vars,
		translate: func(name string) string {
			if name == "python" {
				return vexe
			}
			return name
		}}, nil
}

type Env struct {
	baseURL   *url.URL
	vars      []string
	translate func(string) string
}

func newEnv(conf *Conf, file string) (*Env, error) {
	vars := os.Environ()
	lang := filepath.Ext(file)
	switch lang {
	case ".py":
		return newPythonEnv(conf, vars)
	}
	return nil, fmt.Errorf("unsupported file type %q", lang)
}

func execCommand(name string, args, env []string, verbose bool) error {
	fmt.Printf("Running %s %v\n", name, args)
	cmd := exec.Command(name, args...)
	cmd.Env = env

	output, err := cmd.CombinedOutput()

	if verbose || err != nil {
		fmt.Println(string(output))
	}
	if err != nil {
		return fmt.Errorf("error executing %q %v: %v", name, args, err)
	}
	return nil
}

func startCommand(name string, args, env []string) error {
	fmt.Printf("Starting %s %v\n", name, args)
	cmd := exec.Command(name, args...)
	cmd.Env = env
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		return fmt.Errorf("error executing %q %v: %v", name, args, err)
	}
	return nil
}

func interpret(conf *Conf, env *Env, commands []Command) error {
	for _, command := range commands {
		args := command.args
		switch command.t {
		case "#":
			continue
		case "ENV":
			if len(args) != 2 {
				return fmt.Errorf("ENV: want %q, got %#v", "ENV name value", args)
			}
			name, value := args[0], args[1]
			env.vars = append(env.vars, name+"="+value)
		case "ECHO":
			fmt.Println(strings.Join(args, " "))
		case "SHOW":
			if len(args) != 1 {
				return fmt.Errorf("SHOW: want %q, got %#v", "SHOW file-path", args)
			}
			localPath := args[0]
			if err := showFile(localPath); err != nil {
				return fmt.Errorf("SHOW: %v", err)
			}
		case "FROM":
			if len(args) != 1 {
				return fmt.Errorf("FROM: want %q, got %#v", "FROM base-url", args)
			}
			u, err := url.Parse(args[0])
			if err != nil {
				return fmt.Errorf("FROM: failed parsing URL: %v", err)
			}
			env.baseURL = u
		case "GET":
			var urlPath, localPath string
			if len(args) == 1 {
				urlPath = args[0]
			} else if len(args) == 2 {
				urlPath, localPath = args[0], args[1]
			} else {
				return fmt.Errorf("GET: want %q, got %#v", "GET remote-url [local-path]", args)
			}
			if env.baseURL != nil && !isURL(urlPath) {
				rel, err := url.Parse(urlPath)
				if err != nil {
					return fmt.Errorf("GET: failed parsing URL: %v", err)
				}
				abs := env.baseURL.ResolveReference(rel)
				urlPath = abs.String()
			}
			if _, err := downloadFile(urlPath, localPath); err != nil {
				return fmt.Errorf("GET: %v", err)
			}
		case "FILE":
			localPath, contents := args[0], args[1]
			if err := writeFile(localPath, contents); err != nil {
				return fmt.Errorf("FILE: %v", err)
			}
		case "RUN":
			name, args := args[0], args[1:]
			if err := execCommand(env.translate(name), args, env.vars, conf.verbose); err != nil {
				return fmt.Errorf("RUN: %v", err)
			}
		case "START":
			if !conf.start {
				continue
			}
			name, args := args[0], args[1:]
			if err := startCommand(env.translate(name), args, env.vars); err != nil {
				return fmt.Errorf("START: %v", err)
			}
		default:
			return fmt.Errorf("unknown command %q", command.t)
		}
	}

	return nil
}

func isURL(urlPath string) bool {
	if _, err := url.ParseRequestURI(urlPath); err != nil {
		return false
	}
	if u, err := url.Parse(urlPath); err != nil || u.Scheme == "" || u.Host == "" {
		return false
	}
	return true
}

func getOrLocateMainFile(urlPath string) (string, error) {
	if isURL(urlPath) {
		relPath, err := downloadFile(urlPath, "")
		if err != nil {
			return "", fmt.Errorf("error downloading main file: %v", err)
		}
		return relPath, nil
	}

	if _, err := os.Stat(urlPath); err == nil {
		dir := filepath.Dir(urlPath)
		if dir != "." {
			return "", fmt.Errorf("expected main file to be %q, got %q", filepath.Base(urlPath), urlPath)
		}
		return urlPath, nil
	} else {
		return "", fmt.Errorf("error locating main file: %v", err)
	}
}

func run(conf *Conf, urlPath string) error {
	mainFilePath, err := getOrLocateMainFile(urlPath)
	if err != nil {
		return err
	}

	code, err := readFile(mainFilePath)
	if err != nil {
		return fmt.Errorf("error reading main file: %v", err)
	}

	header, err := parseHeader(code)
	if err != nil {
		return fmt.Errorf("error parsing header: %v", err)
	}

	if len(header.commands) == 0 {
		return errNoHeaderFound
	}

	env, err := newEnv(conf, mainFilePath)
	if err != nil {
		return fmt.Errorf("error initializing environment: %v", err)
	}

	if err := interpret(conf, env, header.commands); err != nil {
		return err
	}

	return nil
}

type Conf struct {
	verbose bool
	start   bool
	python  string
}

func main() {
	var conf Conf

	rootFlagSet := flag.NewFlagSet("nitro", flag.ExitOnError)
	rootFlagSet.BoolVar(&conf.verbose, "verbose", false, "print verbose output")
	rootFlagSet.StringVar(&conf.python, "python", "", "path to the Python executable")
	runFlagSet := flag.NewFlagSet("nitro run", flag.ExitOnError)
	cloneFlagSet := flag.NewFlagSet("nitro clone", flag.ExitOnError)

	runCmd := &ffcli.Command{
		Name:       "run",
		ShortUsage: "nitro [flags] run URL",
		ShortHelp:  "Fetch, set up and run a program.",
		FlagSet:    runFlagSet,
		Exec: func(_ context.Context, args []string) error {
			if n := len(args); n != 1 {
				return flag.ErrHelp
			}
			conf.start = true
			return run(&conf, args[0])
		},
	}

	cloneCmd := &ffcli.Command{
		Name:       "clone",
		ShortUsage: "nitro [flags] clone URL",
		ShortHelp:  "Fetch and set up a program.",
		LongHelp:   "Same as 'nitro run', but skips any START commands during boot.",
		FlagSet:    cloneFlagSet,
		Exec: func(_ context.Context, args []string) error {
			if n := len(args); n != 1 {
				return flag.ErrHelp
			}
			return run(&conf, args[0])
		},
	}

	rootCmd := &ffcli.Command{
		ShortUsage:  "nitro [flags] <subcommand>",
		FlagSet:     rootFlagSet,
		Subcommands: []*ffcli.Command{runCmd, cloneCmd},
		Exec: func(context.Context, []string) error {
			return flag.ErrHelp
		},
	}

	if err := rootCmd.ParseAndRun(context.Background(), os.Args[1:]); err != nil {
		fmt.Fprintf(os.Stderr, "error: %v\n", err)
		os.Exit(1)
	}

}
