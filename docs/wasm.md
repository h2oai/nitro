# Web Assembly

Nitro apps can be run entirely in-browser using *Nitride*, an application runtime for web browsers built
atop [Pyodide](https://pyodide.org).

This means that, in most cases, you can take your existing Nitro app, and repackage it for web browsers so that your
application can be used without hosting it on a server or cloud.

!!! info
    [Pyodide](https://pyodide.org) is a port of [CPython](https://github.com/python/cpython) 
    to [WebAssembly](https://webassembly.org/), and makes it possible to install and run Python packages in the browser.

## Getting started

[Download](https://github.com/h2oai/nitro/releases) and unzip the *Nitride* (Nitro + Pyodide) distribution (named 
`nitride_[VERSION].zip`, for example `nitride_0.11.0.zip`).

The distribution contains the following files:

```
.
├── favicon.ico       # Icon.
├── nitride.js        # Python runtime.
├── static            # Static assets.
│   ├── css           # Built-in styles.
│   └── js            # Front-end.
└── styles.css        # Custom styles.
```

Additionally, the distribution contains several examples, explained later:

```
.
├── example_basic.html
├── example_bokeh.html
├── example_bokeh.py
├── example_bokeh_util.py
├── example_entrypoint.html
├── example_hello.py
└── index.html
```

To run the above examples, you'll need to access them from a web server (and not directly from your computer's file
system).

The simplest way to do that is to open a new terminal, change to the above directory, and launch Python's built-in web
server:

```
cd nitride_[VERSION]
python -m http.server 8000
```

You can then access the examples at https://localhost:8000/.

## Embedding Python in HTML

The simplest way to create an in-browser Nitro app is embed Python in HTML using a `<script type="text/python">` tag.

[example_basic.html](https://github.com/h2oai/nitro/blob/main/py/wasm/examples/example_basic.html):

```html 
<script type="text/python">
from h2o_nitro import AsyncView as View, box

async def main(view: View):
    name = await view(box('What is your name?', value='Boaty McBoatface'))
    feel = await view(box(f'How do you feel today, {name}?', value='intrigued'))
    await view(f'What a coincidence, {name}, I feel {feel}, too!')

nitro = View(main, title='Hello Nitro!', caption='v1.0')
</script>
```

## Loading external modules

Although the above technique works, it's more convenient to write programs in `.py` modules and load them
dynamically.

You can do this easily by adding a `<script type="application/nitro">` tag containing a YAML configuration that describes
your app.

The configuration below loads `example_hello.py` dynamically and executes it (the `entrypoint`).

[example_entrypoint.html](https://github.com/h2oai/nitro/blob/main/py/wasm/examples/example_entrypoint.html):

```html 
<script type="application/nitro">
  language: python
  entrypoint: example_hello.py
</script>
```

[example_hello.py](https://github.com/h2oai/nitro/blob/main/py/wasm/examples/example_hello.py):

```py
from h2o_nitro import AsyncView as View, box

async def main(view: View):
    name = await view(box('What is your name?', value='Boaty McBoatface'))
    feel = await view(box(f'How do you feel today, {name}?', value='intrigued'))
    await view(f'What a coincidence, {name}, I feel {feel}, too!')

nitro = View(main, title='Hello Nitro!', caption='v1.0')
```

## Loading external packages

To load external packages and referenced modules, use `packages`, `bundles`, and `files`.

- `packages` is a list of package names from the Pyodide repository. 
    - [Click here for a complete list of Pyodide packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html).
- `bundles` is a list of pure-Python packages.
    - To include a package from [PyPI](), provide the name of the package (e.g. `numpy` or `pandas`).
    - To include a wheel file, provide the path to the `.whl` file (e.g. `path/to/my/awesome_package-0.42.0-py3-none-any.whl`).
- `files` is a list of `.py` Python modules to download and use.


In the example below, we run [example_bokeh.py](https://github.com/h2oai/nitro/blob/main/py/wasm/examples/example_bokeh.py), 
which depends on [example_bokeh_util.py](https://github.com/h2oai/nitro/blob/main/py/wasm/examples/example_bokeh_util.py), 
`numpy`, `pandas` and `bokeh`.

[example_bokeh.html](https://github.com/h2oai/nitro/blob/main/py/wasm/examples/example_bokeh.html):
```html 
<script type="application/nitro">
  language: python
  packages:
  - numpy
  - pandas
  - bokeh
  bundles:
  - h2o-nitro-bokeh
  files:
  - example_bokeh_util.py
  entrypoint: example_bokeh.py
</script>
```

## Reference

Here are all the configuration options supported by `<script type="application/nitro">`:

```yaml
#
# The programming language to use:
#
language: python
#
# The Pyodide runtime to use for executing Python in the browser:
#
runtime: "https://cdn.jsdelivr.net/pyodide/v0.20.0/full/pyodide.js"
#
# The pre-built packages to load from the Pyodide repository:
# (See https://pyodide.org/en/stable/usage/packages-in-pyodide.html)
#
packages:
- numpy
- pandas
- bokeh
#
# Additional packages to load, if unavailable in the Pyodide repository:
# (Can be names of pure Python packages in PyPI, or paths to wheel files.)
#
bundles:
- nitro-bokeh-plugin
- "path/to/my/awesome_package-0.42.0-py3-none-any.whl"
#
# Additional Python modules or files to copy into the Wasm virtual filesystem:
#
files:
- utils.py
- path/to/something/else.py
#
# The main Python module to load and execute:
#
entrypoint: main.py
#
# Whether the dependencies in the entrypoint module should be 
# detected and loaded automatically:
#
autoload: false
```