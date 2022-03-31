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

## Tour / Docs

Launch the interactive tour / documentation at http://localhost:4999/:

```
nitro tour
```

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

Access your app at http://localhost:5000/.

## Use Tornado or Starlette

New apps created with `nitro create` use Flask by default.

To create a new app using Tornado, run:

```
nitro create my_app --framework tornado
```

To create a new app using Starlette, run:

```
nitro create my_app --framework starlette
```

