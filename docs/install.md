# Getting started

## Installation

Install with interactive tour and documentation:

```
pip3 install h2o-nitro[flask]
```

Or, for a minimal install:

```
pip3 install h2o-nitro
```

## Live Docs

Nitro ships with interactive documentation and live examples:

```
nitro docs
```

Access docs at  [http://localhost:4999/](http://localhost:4999/).

## Create your first app

Create an app named `my_app`:

```
nitro create my_app
```

Launch your app inside a [virtual environment](https://docs.python.org/3/library/venv.html#module-venv):

```
cd my_app
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python app.py
```

Access your app at [http://localhost:5000/](http://localhost:5000/).

## App Templates

To see a list of all available templates, run:

```
nitro list templates
```

## Frameworks

New apps created with `nitro create` use [Flask](https://flask.palletsprojects.com/) by default.

To create a new app using [Tornado](https://www.tornadoweb.org/), run:

```
nitro create my_app --framework tornado
```

To create a new app using [Starlette](https://www.starlette.io/), run:

```
nitro create my_app --framework starlette
```

To see a list of all available frameworks, run:

```
nitro list frameworks
```

