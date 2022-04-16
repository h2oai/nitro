# Nitro

Nitro (N<sub>2</sub>O) is the quickest way to build web apps using Python. No front-end experience required.

![Nitro](docs/assets/banner.png)

## Philosophy

Recall how simple it is to author interactive command line applications using Python's built-in `input()` and `print()`:

```py
def main():
    name = input('What is your name?')
    feel = input(f'How do you feel today, {name}?')
    print(f'What a coincidence, {name}, I feel {feel}, too!')
```

Output:

```
> What is your name?
> Boaty McBoatface
> How do you feel today, Boaty McBoatface?
> intrigued
> What a coincidence, Boaty McBoatface, I feel intrigued, too!
```

Nitro brings that same level of simplicity to authoring web applications:

```py
from h2o_nitro import View, box

def main(view: View):
    name = view(box('What is your name?', value='Boaty McBoatface'))
    feel = view(box(f'How do you feel today, {name}?', value='intrigued'))
    view(f'What a coincidence, {name}, I feel {feel}, too!')
```

![Nitro](docs/assets/images/app-basic.gif)

## Status

H2O Nitro is pre-alpha software. API is subject to change.

## Vision

- **Write once, run anywhere.** Build apps for mobile (iOS, Android), desktop (Linux, OSX, Windows) and the web from one
  codebase, using one language.
- **Write less, do more.** Code is a liability. Less code ≈ less bugs.

## Features

- **No HTML/Javascript.** Build sophisticated multi-page wizard-like workflows and walkthroughs using pure Python.
- **Less Code.** Laser-focused on keeping application code simple, concise, and clear.
    - **Simplicity.** Page flow follows code flow.
    - **Conciseness.** Lowest number of lines of code for expressing solutions to a given problem. bugs.
    - **Clarity.** Write apps without jumping through callbacks, request handlers, or event handlers.
- **Minimal API.** Only three functions: `view()`, `box()`, `option()`, and optionally `row()` and `column()` for
  layout.
- **Batteries-included.** Huge library of sophisticated, accessibility-friendly widgets and data visualizations.
- **Library.** Nitro is a library, not a server. Integrates with [Django](https://www.djangoproject.com/)
  , [Flask](https://flask.palletsprojects.com/), [Starlette](https://www.starlette.io/)
  , [Tornado](https://www.tornadoweb.org/), [Uvicorn](https://www.uvicorn.org/) and other popular frameworks. Can be
  integrated into your existing applications.
- **Prototyping-to-production.** Carefully designed API to rapidly prototype new ideas, then progressively improve
  presentation and aesthetics over time without affecting initial implementation simplicity, or sacrificing control.
- **Unix philosophy.** Tries to do one thing and do it well: display interactive user interfaces. Bring your own web
  app/server of choice and follow its recommendations for hosting, deployment, security, monitoring, metrics and data
  management.
- **Extensively documented.** Run `nitro docs` to access interactive docs and 150+ live examples.

## Differences from H<sub>2</sub>O Wave

**TL;DR:** Use [Wave](https://wave.h2o.ai/) for building visualization-heavy analytical dashboards. For everything else,
use Nitro.

- **Deployment.** Nitro is a library, not a server. It's a heavily stripped-down version of [Wave](https://wave.h2o.ai/)
  with a different, simpler API, designed for integration with existing frameworks, and cross-compiling for mobile and
  desktop apps.
- **Content Management.** Wave is capable of storing and broadcasting content and data, making it simple to build
  dashboards without having to deal with data management. Nitro has no such features.
- **API.** Wave's API is *dashboard-oriented*, and has several features that make it easy to develop and deploy
  real-time analytics and dashboards easily. Nitro's API is *page-flow-oriented*, and makes it radically simple to
  author sophisticated workflows and wizards without dealing with callback functions and request handlers.


## Getting started

### Installation

Install with interactive tour and documentation:

```
pip3 install "h2o-nitro[flask]"
```

Or, for a minimal install:

```
pip3 install h2o-nitro
```

### Live Docs

Nitro ships with interactive documentation and live examples:

```
nitro docs
```

Access docs at  [http://localhost:4999/](http://localhost:4999/).

### Create your first app

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

### Change starter app

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

### Change framework

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



## Guide

You can always view the docs for the latest version at https://nitro.h2o.ai/.

- [Basics](docs/basics.md)
- [Markdown](docs/markdown.md)
- [Styling](docs/styling.md)
- [Images](docs/images.md)
- [Layout](docs/layout.md)
- [Forms](docs/forms.md)
- [Textbox](docs/textbox.md)
- [Spinbox](docs/spinbox.md)
- [Checkbox](docs/checkbox.md)
- [Pickers](docs/pickers.md)
- [Options](docs/options.md)
- [Buttons](docs/buttons.md)
- [Radio Buttons](docs/radio-buttons.md)
- [Dropdown](docs/dropdown.md)
- [Dropdown List](docs/dropdown-list.md)
- [Checklist](docs/checklist.md)
- [Slider](docs/slider.md)
- [Range Slider](docs/range-slider.md)
- [Time Picker](docs/time-picker.md)
- [Date Picker](docs/date-picker.md)
- [Calendar](docs/calendar.md)
- [Week Picker](docs/week-picker.md)
- [Month Picker](docs/month-picker.md)
- [Tag Picker](docs/tag-picker.md)
- [Color Picker](docs/color-picker.md)
- [Color Palette](docs/color-palette.md)
- [Rating](docs/rating.md)
- [Theming](docs/theming.md)
- [Advanced Layout](docs/advanced-layout.md)