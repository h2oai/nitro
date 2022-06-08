# Examples

It's easy to run these examples on your computer.

1. [Install](install.md) `nitro`.
2. Create and switch to a new directory, say, `nitro_examples`.
3. Execute `nitro run http://path/to/example.py`.

!!! info 
    If you run multiple examples from the same working directory, `nitro run` will reuse the virtual environment 
    already present in that directory.

!!! tip
    If you simply want to fetch, but not run the example, use `nitro clone` instead of `nitro run`.

## Basic Examples

**[Hello World using Flask](https://github.com/h2oai/nitro/blob/main/py/examples/hello.py)**

A simple app, using [Flask](https://flask.palletsprojects.com/).

```
nitro run https://raw.githubusercontent.com/h2oai/nitro/main/py/examples/hello.py
```

**[Hello World using Tornado](https://github.com/h2oai/nitro/blob/main/py/examples/hello_tornado.py)**

Same example as above, but using [Tornado](https://www.tornadoweb.org/en/stable/index.html).

```
nitro run https://raw.githubusercontent.com/h2oai/nitro/main/py/examples/hello_tornado.py
```

**[Hello World using Starlette](https://github.com/h2oai/nitro/blob/main/py/examples/hello_starlette.py)**

Same example as above, but using [Starlette](https://www.starlette.io/) and [Uvicorn](https://www.uvicorn.org/).

```
nitro run https://raw.githubusercontent.com/h2oai/nitro/main/py/examples/hello_starlette.py
```

**[Apply for Space Flight](https://github.com/h2oai/nitro/blob/main/py/examples/space_flight.py)**

A job application wizard. Seven pages in seven statements!

```
nitro run https://raw.githubusercontent.com/h2oai/nitro/main/py/examples/space_flight.py
```

