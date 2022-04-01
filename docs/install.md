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

## Change starter app

`nitro create` creates the simplest possible app by default, but you can start from other kinds of sample
apps.

Create an app that lets you apply for space flight, with multiple workflows, a menu and navbar.

```
nitro create my_app --template recruitment
```

To see a list of all available starter app templates, run:

```
nitro list templates
```

## Change framework

New apps created with `nitro create` use [Flask](https://flask.palletsprojects.com/) by default, but you can use other
frameworks, too.

Create an app using [Tornado](https://www.tornadoweb.org/):

```
nitro create my_app --framework tornado
```

Create an app using [Starlette](https://www.starlette.io/):

```
nitro create my_app --framework starlette
```

To see a list of all available frameworks, run:

```
nitro list frameworks
```

