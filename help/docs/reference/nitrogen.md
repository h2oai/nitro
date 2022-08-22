---
template: overrides/main.html
---
# Nitrogen

*Nitrogen* is a simple mini-language used by `nitro run` to set up and launch apps.

It's similar in principle to Dockerfiles, and enables you to author and share single-file plain-Python programs that can be easily
set up and launched by others without having to read through a pile of installation instructions. 

You can think of Nitrogen as a peer-to-peer software distribution tool that eliminates manual installs and updates.

!!!tip
    It's not necessary to learn Nitrogen for developing Nitro apps, but it's useful if you want to share your 
    single-file app with others in the form of [gists](https://gist.github.com/) or 
    [snippets](https://gitlab.com/explore/snippets).

## Format

Nitrogen instructions are placed inside a comment block, usually at the top of a file, 
enclosed between two `===` (triple-equals) comments:

```py
# ===
# (Stuff)
# ===
```

The header has three parts:

1. (Optional) YAML metadata.
2. A `Setup:` attribute.
3. Nitrogen instructions.

Like this:

```py
# ===
# (YAML metadata, optional)
# Setup:
# (Nitrogen instructions)
# ===
```

Here's a minimal example without metadata. It simply prints "Hello World!":

```py 
# ===
# Setup:
# ECHO Hello World!
# ===
```

Here's a more complete example, with metadata:

```py
# ===
# About: Hello World
# Author: Boaty McBoatface
# Setup:
# FILE requirements.txt EOF
# flask
# simple-websocket
# h2o-nitro
# EOF
# RUN python -m pip install -r requirements.txt
# ENV FLASK_APP hello.py
# START python -m flask --debug run
# ===
```


Lines starting with `#` are ignored. The following example prints only "Bob"

```py 
# ===
# Setup:
# # ECHO Alice
# ECHO Bob
# ===
```

Long lines can be broken into multiple lines using a `\` at the end of a line. The following examples are equivalent:

```py 
# ===
# Setup:
# ECHO Hello World!
# ===
```

```py 
# ===
# Setup:
# ECHO Hello\
#  World!
# ===
```

## Instructions

Instructions have the following form:

```
INSTRUCTION argument1 argument2 argument3 ...
```

Arguments containing whitespace can be quoted, like this:

```
INSTRUCTION argument1 "argument 2" argument3 ...
```

The instruction is not case-sensitive. but UPPERCASE is preferred for readability.

Instructions **must** begin with a `Setup:`, and are run in order. If an error is encountered, `nitro run` is aborted.

!!!attention

    **For instructions that accept file paths:** 
    `file-path` must be relative and slash-separated for platform independence 
    (`path/to/file`, not `\path\to\file` or `/path/to/file`).
    The path is automatically translated to the correct format required by the target platform.

    File operations outside the current working directory are not allowed.


### ECHO

```
ECHO arguments...
```

`ECHO` prints its arguments. 

!!!example

    Print "Hello World!"

    ```
    ECHO Hello World!
    ```

### FILE

```
FILE file-path eof-marker
line1
line2
...
lineN
eof-marker
```

`FILE` writes a text file at `file-path` containing everything in between the two `eof-marker` tokens.

`file-path` must be relative and slash-separated (`path/to/file`, not `\path\to\file` or `/path/to/file`) for platform independence.
The path is automatically translated to the correct format required by the target platform.

!!!example

    Write three lines to `requirements.txt`:

    ```
    FILE requirements.txt EOF
    flask
    simple-websocket
    h2o-nitro
    EOF
    ```

### GET

```
GET url [file-path]
```

`GET` fetches a file from a `http://` or `https://` URL and saves it at `file-path`. 

`GET` is useful for fetching any additional files related to the app, 
like datasets, configuration files, images, or even other source files.

If `file-path` is not provided, the filename is deduced from the URL. 
If `file-path` is a directory (ends with a `/`), the filename is deduced from the URL and written to the directory.

!!!example

    Fetch a file and save it to `license.txt`:

    ```
    GET https://raw.githubusercontent.com/path/to/license.txt
    ```

!!!example

    Fetch a file and save it to `files/license.txt`:

    ```
    GET https://raw.githubusercontent.com/path/to/license.txt files/
    ```

!!!example

    Fetch `license.txt` and save it to `files/app-license.txt`:

    ```
    GET https://raw.githubusercontent.com/path/to/license.txt files/app-license.txt
    ```

### FROM

```
FROM base-url
```

`FROM` sets a base URL for subsequent `GET` instructions.

The primary function of `FROM` is to simplify repetitive `GET` instructions.

!!!example "Before"

    ```
    GET https://raw.githubusercontent.com/path/to/foo.txt
    GET https://raw.githubusercontent.com/path/to/bar.txt
    GET https://raw.githubusercontent.com/path/to/qux.txt
    ```

!!!example "Improved"

    ```
    FROM https://raw.githubusercontent.com/path/to
    GET foo.txt
    GET bar.txt
    GET qux.txt
    ```


### SHOW

```
SHOW file-path
```

`SHOW` prints the contents of a file, similar to `cat` on Unix or `type` on Windows.

!!!example

    Print the contents of `license.txt`

    ```
    SHOW license.txt
    ```

### ENV

```
ENV name value
```

`ENV` sets the environment variable named `name` to value `value`.

!!!example

    Set `FLASK_APP=hello.py` and `FLASK_SESSION_COOKIE_NAME=crumbles`:

    ```
    ENV FLASK_APP hello.py
    ENV FLASK_SESSION_COOKIE_NAME crumbles
    ```

### RUN

```
RUN command argument1 argument2 argument3 ...
```

`RUN` executes a command. If an error is encountered or `-verbose` is set, it prints `STDERR` and `STDOUT`.

!!!example

    Run `python -m pip install -r requirements.txt`:

    ```
    RUN python -m pip install -r requirements.txt
    ```

### START

```
START command argument1 argument2 argument3 ...
```

`START` is similar to `RUN`, except that it streams `STDERR` and `STDOUT` to the terminal. 

It is typically used for the final instruction in a file for launching long-running services 
like Flask, Tornado, Starlette, etc. where it's useful to inspect the command's output while running.


!!!example

    Run `python -m flask run`:

    ```
    START python -m flask run
    ```
