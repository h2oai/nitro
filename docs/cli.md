# Nitro CLI

The best way to get better at programming is to clone other apps and tinker with them.
[Read the source, Luke](https://blog.codinghorror.com/learn-to-read-the-source-luke/)!

The `nitro` CLI (command line interface) makes it really easy to play with any Nitro app published anywhere on the world wide web.

!!! tip

    You don't need the `nitro` CLI to develop or deploy Nitro apps. 
    It's simply a tool to easily clone, set up and run examples and apps shared on the internet.

!!! caution

    Using `nitro run` to execute code is no different than using `python` to execute code.
    Do not use `nitro run` to execute someone else's code without reading it first!
    **Make sure you trust the authors.** 

## Installation

1. Go to [https://github.com/h2oai/nitro/releases](https://github.com/h2oai/nitro/releases).
2. Download the appropriate archive for your platform.
3. Extract the archive and move `nitro` or `nitro.exe` to a location that's in your `PATH`. [Learn how.](help.md#add-cli-to-path)

!!! success "Test your installation"
    To verify if `nitro` is accessible, open a new terminal window and run `nitro version`.

## Run an app

From your terminal, create and switch to a new directory:

```bash
mkdir my_app
cd my_app
```

Run a "Hello World" app:

```bash
nitro run https://raw.githubusercontent.com/h2oai/nitro/main/py/examples/hello.py
```

The `nitro run` command does several things for you:

- Creates a new virtual environment.
- Ensures that a current version of `pip` is available.
- Installs all the libraries that `hello.py` needs.
- Launches the app.

```txt
Downloading https://raw.githubusercontent.com/h2oai/nitro/main/py/examples/hello.py
Downloaded hello.py: 1.5 kB
Creating virtual environment using "/usr/bin/python3" ...
Running /usr/bin/python3 [-m venv venv] ...
Found "venv/bin/python" in virtual environment.
Bootstrapping pip ...
Running venv/bin/python [-m ensurepip --upgrade] ...
Running venv/bin/python [-m pip install -r requirements.txt] ...
Starting venv/bin/python [-m flask run] ...
 * Serving Flask app 'hello.py' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 140-120-041
```

!!! success "Play with the app"
    Go to [http://localhost:5000/](http://localhost:5000/).

## Edit the app

To see what `nitro run` just did, let's inspect the directory's contents. You should see:

- `venv`: A [virtual environment](https://docs.python.org/3/library/venv.html) for the libraries used by the app.
- `requirements.txt`: A [requirements file](https://pip.pypa.io/en/stable/user_guide/#requirements-files) containing a
  list of installed libraries.
- `hello.py`: The [app's source code](https://github.com/h2oai/nitro/blob/main/py/examples/hello.py).

Open the directory in a Python editor, like [PyCharm](https://www.jetbrains.com/pycharm/)
or [Visual Studio Code](https://code.visualstudio.com/). Then, make some change to `hello.py` and save. You should see
your browser reload and display your changes automatically!

!!! tip
    `nitro run` can run any Nitro app hosted anywhere on the world wide web, including [gists](https://gist.github.com/)
    and [snippets](https://gitlab.com/explore/snippets), which makes sharing your apps just as easy as running them.

## It's just Python!

If you inspect `hello.py`, you'll see that it's a plain Python file containing a
simple [Flask](https://flask.palletsprojects.com/) app and a [Nitrogen](nitrogen.md) header:

```py
# Flask imports go here.

from h2o_nitro import View, box, web_directory


def main(view: View):
    name = view(box('What is your name?', value='Boaty McBoatface'))
    feel = view(box(f'How do you feel today, {name}?', value='intrigued'))
    view(f'What a coincidence, {name}, I feel {feel}, too!')


nitro = View(main, title='Hello Nitro!', caption='v1.0')

# Flask initialization goes here.
```

You can run `hello.py` using `nitro run` (`nitro run` accepts local files in addition to URLs):

```
nitro run hello.py
```

Or, if you prefer to use Python directly:

=== "Linux / macOS"

    ```
    source venv/bin/activate
    python hello.py
    ```

=== "Windows"


    ```
    .\env\Scripts\activate
    python hello.py
    ```

There's no magic here. Nitro apps are just plain Python programs.

## How does it work?

The `nitro run` command looks for and executes [Nitrogen](nitrogen.md) instructions in the source file's comments.

Nitrogen is a mini-language that describes libraries to install, files to fetch, and commands to run in order to 
set up and launch the app.

[Read the Nitrogen specifications](nitrogen.md) to learn more.

## Upgrading

Upgrades are easy: simply [download a new release](https://github.com/h2oai/nitro/releases) and replace your old copy
of `nitro`.

