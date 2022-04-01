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

### Basics - Hello World!

Call `view()` to show something on a page.


```py
view('Hello World!')
```


Here, `view()` is comparable to Python's built-in `print()` function,
and prints its arguments to the web page.

### Basics - Formatting content

Strings passed to `view()` are interpreted as
[Markdown](https://github.github.com/gfm/)


```py
view('_Less_ `code` means _less_ **bugs**.')
```

### Basics - Show multiline content

Triple-quote strings to pass multiple lines of markdown.


```py
view('''
The King said, very gravely:
- Begin at the beginning,
- And go on till you come to the end,
- Then stop.
''')
```

### Basics - Show items at once

Pass multiple arguments to `view()` to lay them out top to bottom.


```py
view(
    'Begin at the beginning,',
    'And go on till you come to the end,',
    'Then stop.',
)
```

### Basics - Show items one at a time

Call `view()` multiple times to show items one at a time.

The following example steps through three different pages.


```py
view('Begin at the beginning,')
view('And go on till you come to the end,')
view('Then stop.')
```

### Basics - Get user input

Call `box()` to create a *box* (an input field) and pass it to `view()`.

When a view contains a box, the `view()` function returns its input value.

`box()` creates a textbox by default, but can also create other kinds of input fields, like checkboxes,
dropdowns, spinboxes, buttons, calendars, etc.


```py
# Display a textbox and assign the entered value to a variable.
name = view(box('What is your name?', value='Boaty McBoatface'))
# Print the entered value.
view(f'Hello, {name}!')
```


Here, `view()` behaves similar to Python's built-in `input()` function.

### Basics - Get inputs one at a time

Call `view()` multiple times to prompt for a sequence of inputs, one at a time.

The following example steps through three different pages.


```py
# Prompt for first name.
first_name = view(box('First name', value='Boaty'))
# Prompt for last name.
last_name = view(box('Last name', value='McBoatface'))
# Print the entered values.
view(f'Hello, {first_name} {last_name}!')
```

### Basics - Get inputs at once

Pass multiple boxes to `view()` to prompt for inputs at once.

When a view contains multiple boxes, the `view()` function returns multiple values, in order.


```py
# Prompt for first and last names.
first_name, last_name = view(
    box('First name', value='Boaty'),
    box('Last name', value='McBoatface'),
)
# Print the entered values
view(f'Hello, {first_name} {last_name}!')
```

### Basics - Putting it all together

Views can be chained together to create sophisticated workflows and wizards.

The example below shows a simple online ordering system.

Observe how it combines `view()` with conditionals and loops, while keeping the code
simple, concise, and clear.

Notably, if you have built web applications before, notice the absence of callbacks, event handlers,
web request handlers, routing, etc.


```py
# Our menu.
menu = dict(
    Donut=['Plain', 'Glazed', 'Chocolate'],
    Coffee=['Dark-roast', 'Medium-roast', 'Decaf'],
)

# Prompt for items.
items = view(box(
    'What would you like to order today?',
    options=list(menu.keys()),  # Menu item names.
    multiple=True,  # Allow multiple selections.
))

if len(items) == 0:  # Nothing selected.
    view(f'Nothing to order? Goodbye!')
    return

# The order summary, which we'll display later.
summary = ['### Order summary:']

# Prompt for counts and flavors.
for item in items:
    count = view(box(f'How many orders of {item} would you like?', value=3))
    for i in range(count):
        flavor = view(box(
            f'Pick a flavor for {item} #{i + 1}',
            options=menu[item],
        ))
        summary.append(f'1. {flavor} {item}')

summary.append('\nThank you for your order!')

# Finally, show summary.
view('\n'.join(summary))
```


Building a similar multi-page interactive app with a regular web framework can be
a fairly complex endeavor, weaving together requests and replies with logic spread across
multiple functions , but Nitro makes all this delightfully simple!

### Markdown - Basics

Strings passed to `view()` are interpreted as [Github Flavored Markdown](https://github.github.com/gfm/) (GFM).


```py
view('''
# Heading 1
## Heading 2
### Heading 3 
#### Heading 4
##### Heading 5 
###### Small print

This is a paragraph, with **bold**, *italics* 
(or _italics_), ***important***, `code`
and ~~strikethrough~~ formatting.

Here's a [hyperlink](https://example.com) to https://example.com.

![An image](https://picsum.photos/200)

> This is a block quote.

- List item 1
- List item 2
  - Sublist item 1
  - Sublist item 2
- List item 3

1. Numbered list item 1
1. Numbered list item 2
  1. Sublist item 1
  1. Sublist item 2
1. Numbered list item 3

Here is a footnote[^1] and another one[^another].

[^1]: A reference.
[^another]: Another reference.
''')
```


Any uniform indentation is automatically ignored.

### Markdown - Links as inputs

Local links in markdown content behave just like any other input.

Clicking on a local link returns the name of the link.


```py
choice = view('''
Pick a flavor:
- [Vanilla](#vanilla)
- [Strawberry](#strawberry)
- [Chocolate](#chocolate)

Or, [surprise me](#surprise-me)!
''')
view(f'You clicked on {choice}.')
```

### Markdown - Syntax highlighting

Code blocks in Markdown support syntax highlighting for 180+ languages using [highlight.js](https://highlightjs.org/).

To enable syntax highlighting, suffix the language to the opening triple-backticks.

[See list of supported languages](https://github.com/highlightjs/highlight.js/blob/main/SUPPORTED_LANGUAGES.md).


```py
def markdown_syntax_highlighting(view: View):
    view('''
    Python:
    ```py
    def hello():
        print('Hello!')
    ```

    Javascript:
    ```js
    function hello() {
        console.log('Hello!');
    }
    ```
    ''')
```

### Layout - Basics

By default each item passed to `view()` are laid out one below the other, with a 10px gap.


```py
view(
    box(value='Top'),
    box(value='Middle'),
    box(value='Bottom'),
)
```

### Layout - Rows

Use `row()` to lay out multiple items horizontally, left to right.

By default, items take up equal amounts of space, with a `10px` gap between the items.


```py
view(row(
    box(value='Left'),
    box(value='Center'),
    box(value='Right'),
))
```


Setting `row=True` produces the same result as wrapping items with `row()`.


```py
view(
    box(value='Left'),
    box(value='Center'),
    box(value='Right'),
    row=True,
)
```

### Layout - Columns

Use `col()` to lay out multiple items vertically, top to bottom.

The example shows one row split into three columns containing three rows each.


```py
view(
    row(
        col(
            box(value='North-west'),
            box(value='West'),
            box(value='South-west'),
        ),
        col(
            box(value='North'),
            box(value='Center'),
            box(value='South'),
        ),
        col(
            box(value='North-east'),
            box(value='East'),
            box(value='South-east'),
        ),
    ),
)
```

### Layout - Background Color

Set `background=` to apply a background color.

The text color is automatically changed to a contrasting color if not specified.
A `10px` padding is automatically applied if not specified.


```py
text = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
do eiusmod tempor incididunt ut labore et dolore magna aliqua.
'''
view(
    box(text, background='#e63946'),
    box(text, background='#f1faee'),
    box(text, background='#a8dadc'),
    box(text, background='#457b9d'),
    box(text, background='#1d3557'),
)
```

### Layout - Text Color

Set `color=` to change the text color.


```py
text = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
do eiusmod tempor incididunt ut labore et dolore magna aliqua.
'''
view(
    box(text, color='#e63946'),
    box(text, color='#457b9d'),
    box(text, color='#1d3557'),
)
```

### Layout - Border Color

Set `border=` to add a border.

A `10px` padding is automatically applied if not specified.


```py
text = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
do eiusmod tempor incididunt ut labore et dolore magna aliqua.
'''
view(
    box(text, border='#e63946'),
    box(text, border='#457b9d'),
    box(text, border='#1d3557'),
)
```

### Layout - Align Text

Set `align=` to `left`, `right`, `center` or `justify` to align text.


```py
text = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
'''
view(
    row(
        box(text, align='left'),
        box(text, align='center'),
        box(text, align='justify'),
        box(text, align='right'),
        gap=20,
    )
)
```

### Layout - Sizing

Nitro provides extensive control over how items are sized and spaced, using `width`, `height`, `margin`, `padding`,
and `gap`.

These parameters can be specified as either integers or strings.

- Integers are interpreted as pixels, e.g. `42` and `'42px'` have the same effect.
- Strings must be a number followed by one of the units listed below (e.g. `'42px'`, `'42in'`, `'42mm'`, etc.
- Absolute units:
- `px`: One pixel (1/96th of an inch).
- `cm`: One centimeter.
- `mm`: One millimeter.
- `in`: One inch (96px).
- `pc`: One pica (12pt or 1/6th of an inch).
- `pt`: One point (1/72nd of an inch).
- Relative units:
- `%`: A percentage of the container's size.
- `vh`: 1% of the viewport height.
- `vw`: 1% of the viewport width.
- `vmin`: The smaller of `vw` and `vh`.
- `vmax`: The larger of `vw` and `vh`.
- `ex`: The x-height of the font of the element.
- `em`: The font size of the element.
- `rem`: The font size of the page.


```py
text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
view(
    box(text, width=200, background='#eee'),  # interpreted as '200px'
    box(text, width='250px', background='#eee'),
    box(text, width='3in', background='#eee'),
    box(text, width='50%', background='#eee'),
    box(text, height='1in', background='#eee'),
    box(text, width='250px', height='100px', background='#eee'),
)
```

### Layout - Gap

Set `gap=` to control the spacing between items. The default gap is `10` or `'10px'`.


```py
view(
    box(value='Top'),
    box(value='Middle'),
    box(value='Bottom'),
    gap=25,
)
```

### Layout - Margin

Set `margin=` to add a margin around each item.

Top, right, bottom, left margins can be controlled independently, and are specified
as `'top right bottom left'` strings.

- `'x'` is shorthand for `'x x x x'`.
- `'x y'` is shorthand for `'x y x y'`.
- `'x y z'` is shorthand for `'x y z y'`.


```py
text = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
do eiusmod tempor incididunt ut labore et dolore magna aliqua.
'''
boxes = [
    # Uniform 20px margin
    box(text, margin='20px', background='#eee'),
    # Same as '20px'
    box(text, margin=20, background='#eee'),
    # 0px top and bottom, 100px right and left margin
    box(text, margin='0px 100px', background='#eee'),
    # 0px top, 100px right and left, 30px bottom margin
    box(text, margin='0px 100px 30px', background='#eee'),
    # 0px top, 100px right, 30px bottom, 200px left margin
    box(text, margin='0px 100px 30px 200px', background='#eee'),
]
view(col(*[row(b, border='#000', padding=0) for b in boxes]))
```

### Layout - Padding

Set `padding=` to control the padding (inset) inside each item.

Top, right, bottom, left paddings can be controlled independently, and are specified
as `'top right bottom left'` strings.

- `'x'` is shorthand for `'x x x x'`.
- `'x y'` is shorthand for `'x y x y'`.
- `'x y z'` is shorthand for `'x y z y'`.


```py
text = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
do eiusmod tempor incididunt ut labore et dolore magna aliqua.
'''
view(
    col(
        # Uniform 20px padding
        box(text, padding='20px', background='#eee'),
        # Same as '20px'
        box(text, padding=20, background='#eee'),
        # 0px top and bottom, 100px right and left padding
        box(text, padding='0px 100px', background='#eee'),
        # 0px top, 100px right and left, 30px bottom padding
        box(text, padding='0px 100px 30px', background='#eee'),
        # 0px top, 100px right, 30px bottom, 200px left padding
        box(text, padding='0px 100px 30px 200px', background='#eee'),
    )
)
```

### Layout - Tile

Set `tile=` to control how items inside a view, row, or column are tiled along the main axis.

- The main axis for a row is horizontal, starting at the left, and ending at the right.
- The main axis for a column is vertical, starting at the top, and ending at the bottom

`tile=` can be set to `start`, `center`, `end`, `between`, `around`, `evenly`, 'stretch', or `normal`.


```py
boxes = [box(text=f'{i + 1}', background='#666', width=100) for i in range(3)]
row_style = dict(background='#eee')
view(
    # Pack items from the start.
    row(*boxes, tile='start', **row_style),

    # Pack items around the center.
    row(*boxes, tile='center', **row_style),

    # Pack items towards the end.
    row(*boxes, tile='end', **row_style),

    # Distribute items evenly.
    # The first item is flush with the start,
    # the last is flush with the end.
    row(*boxes, tile='between', **row_style),

    # Distribute items evenly.
    # Items have a half-size space on either side.
    row(*boxes, tile='around', **row_style),

    # Distribute items evenly.
    # Items have equal space around them.
    row(*boxes, tile='evenly', **row_style),

    # Default alignment.
    row(*boxes, tile='normal', **row_style),
)
```

### Layout - Cross-tile

Set `cross_tile=` to control how items inside a view, row, or column are tiled along the cross axis.

- The cross axis for a row is vertical. starting at the top, and ending at the bottom
- The cross axis for a column is horizontal, starting at the left, and ending at the right.

`cross_tile=` can be set to `start`, `center`, `end`, `stretch`, or `normal`.


```py
boxes = [box(text=f'{i + 1}', background='#666', width=100) for i in range(3)]
col_style = dict(height=100, background='#eee')
view(
    # Pack items from the start.
    col(row(*boxes, cross_tile='start'), **col_style),

    # Pack items around the center.
    col(row(*boxes, cross_tile='center'), **col_style),

    # Pack items towards the end.
    col(row(*boxes, cross_tile='end'), **col_style),

    # Stretch items to fit.
    col(row(*boxes, cross_tile='stretch'), **col_style),

    # Default alignment.
    col(row(*boxes, cross_tile='normal'), **col_style),
)
```

### Layout - Wrap

Set `wrap=` to control how items are wrapped inside a view, row, or column.

`wrap=` can be set to `start`, `center`, `end`, `between`, `around`, `evenly`, 'stretch', or `normal`.


```py
boxes = [box(text=f'{i + 1}', background='#666', width=150, height=50) for i in range(9)]
row_style = dict(height=300, background='#eee')
view(
    # Pack items from the start.
    row(*boxes, wrap='start', **row_style),

    # Pack items around the center.
    row(*boxes, wrap='center', **row_style),

    # Pack items towards the end.
    row(*boxes, wrap='end', **row_style),

    # Distribute items evenly.
    # The first item is flush with the start,
    # the last is flush with the end.
    row(*boxes, wrap='between', **row_style),

    # Distribute items evenly.
    # Items have a half-size space on either side.
    row(*boxes, wrap='around', **row_style),

    # Distribute items evenly.
    # Items have equal space around them.
    row(*boxes, wrap='evenly', **row_style),

    # Default alignment.
    row(*boxes, wrap='normal', **row_style),
)
```

### Layout - Grow and Shrink

Set `grow=` or `shrink=` to specify what amount of the available space the item should take up
inside a view, row, or column.

Setting `grow=` expands the item. Setting `shrink=` contracts the item. Both are proportions.

By default, items are grown or shrunk based on their initial size. To resize them on a different basis,
set `basis=` to the value you want.

- `basis=0` means "distribute available space assuming that the initial size is zero".
- `basis='20px'` means "distribute available space assuming that the initial size is 20px".
- The default behavior (if `basis=` is not set) is to assume that the initial size is the size of the item's content.


```py
box_style = dict(background='#666')
row_style = dict(background='#eee')
view(
    '1:?:?',
    row(
        # Take up all available space.
        box('a', grow=1, **box_style),
        box('b', width=50, **box_style),
        box('c', width=50, **box_style),
        **row_style,
    ),
    '1:1:?',
    row(
        # Take up one part of available space = 1 / (1 + 1).
        box('a', grow=1, **box_style),
        # Take up one part of available space = 1 / (1 + 1).
        box('b', grow=1, **box_style),
        box('c', width=50, **box_style),
        **row_style,
    ),
    '2:1:?',
    row(
        # Take up two parts of available space = 2 / (2 + 1).
        box('a', grow=2, **box_style),
        # Take up one part of available space = 1 / (2 + 1).
        box('b', grow=1, **box_style),
        box('c', width=50, **box_style),
        **row_style,
    ),
    '1:2:3:?',
    row(
        # Take up one part of available space = 1 / (1 + 2 + 3).
        box('a', grow=1, **box_style),
        # Take up two parts of available space = 2 / (1 + 2 + 3).
        box('b', grow=2, **box_style),
        # Take up three parts of available space = 3 / (1 + 2 + 3).
        box('c', grow=3, **box_style),
        box('d', width=50, **box_style),
        **row_style,
    ),
    '1:1:1:1',
    row(
        # Divide available space equally.
        box('a', grow=1, **box_style),
        box('b', grow=1, **box_style),
        box('c', grow=1, **box_style),
        box('d', grow=1, **box_style),
        **row_style,
    ),
)
```

### Forms - Basic

To create a form, simply lay out all the inputs you need inside a view, then destructure the return value in order.


```py
username, password, action = view(
    box('Username', value='someone@company.com'),
    box('Password', value='pa55w0rd', password=True),
    box(['Login']),
)
view(f'You entered `{username}`/`{password}` and then clicked on {action}.')
```

### Forms - Horizontal

Wrap items with `row()` to lay them out left to right.
There is no change to the way the return values are destructured.


```py
username, password, action = view(
    row(
        box('Username', value='someone@company.com'),
        box('Password', value='pa55w0rd', password=True),
        box(['Login']),
    )
)
view(f'You entered `{username}`/`{password}` and then clicked on {action}.')
```

### Forms - Combined

Use `row()` and `col()` to mix and match how items are laid out. Destructure the return values in the same order.


```py
first, last, addr1, addr2, city, state, zip, action = view(
    row(box('First name', value=''), box('Last name', value='')),
    box('Address line 1', value=''),
    box('Address line 2', value=''),
    row(box('City', value=''), box('State', value=''), box('Zip', value='')),
    box([
        option('yes', 'Sign me up!', selected=True),
        option('no', 'Not now'),
    ])
)
view(f'''
You provided:

Address: {first} {last}, {addr1}, {addr2}, {city} {state} {zip}

Sign up: {action}
''')
```

### Forms - Improved

Specify additional layout parameters like `width=`, `grow=`, etc. to get more control over
how items are laid out.


```py
first, middle, last, addr1, addr2, city, state, zip, action = view(
    row(box('First name', value=''), box('M.I.', value='', width='10%'), box('Last name', value='')),
    box('Address line 1', value=''),
    box('Address line 2', value=''),
    row(box('City', value='', grow=5), box('State', value='', width='20%'), box('Zip', value='', grow=1)),
    box([
        option('yes', 'Sign me up!', caption='Terms and conditions apply', selected=True),
        option('no', 'Not now', caption="I'll decide later"),
    ])
)
view(f'''
You provided:

Address: {first} {middle} {last}, {addr1}, {addr2}, {city} {state} {zip}

Sign up: {action}
''')
```

### Textbox - Basic

Call `box()` with `mode='text'` to show a textbox.

The return value is the text entered into the box.


```py
x = view(box(mode='text'))
view(f'You entered {x}.')
```

### Textbox - Value

Set `value=` to prefill the box with a value.

`mode='text'` can be elided if `value=` is set.


```py
speed = view(box(value='60 km/h'))
view(f'Your speed is {speed} km/h.')
```

### Textbox - Label

Any text passed to `box()` is used as a label.


```py
speed = view(box('Speed', value='60'))
view(f'Your speed is {speed} km/h.')
```

### Textbox - Placeholder

Use `placeholder=` to show placeholder text inside the box.


```py
speed = view(box('Speed', placeholder='0 km/h'))
view(f'Your speed is {speed} km/h.')
```

### Textbox - Required

Set `required=True` to indicate that input is required.


```py
speed = view(box('Speed (km/h)', required=True))
view(f'Your speed is {speed} km/h.')
```

### Textbox - Input Mask

Set `mask=` to specify an input mask. An input mask is used to format the text field
for the expected entry.

For example, to accept a phone number, use an input mask containing three sets of digits.


```py
phone = view(box('Phone', mask='(999) 999 - 9999'))
view(f'Your phone number is {phone}.')
```


To construct the input mask:

- Use `a` to indicate a letter.
- Use `9` to indicate a number.
- Use `*` to indicate a letter or number.
- Use a backslash to escape any character.

### Textbox - Icon

Set `icon=` to show an icon at the end of the box.


```py
phrase = view(box('Filter results containing:', icon='Filter'))
view(f'You set a filter on `{phrase}`.')
```

### Textbox - Prefix

Set `prefix=` to show a prefix at the start of the box.


```py
website = view(box('Website', prefix='https://', value='example.com'))
view(f'Your website is https://{website}.')
```

### Textbox - Suffix

Set `suffix=` to show a suffix at the end of the box.


```py
website = view(box('Website', suffix='.com', value='example'))
view(f'Your website is {website}.com.')
```

### Textbox - Prefix and Suffix

A textbox can show both a prefix and a suffix at the same time.


```py
website = view(box('Website', prefix='https://', suffix='.com', value='example'))
view(f'Your website is https://{website}.com.')
```

### Textbox - Error

Set `error=` to show an error message below the box.


```py
speed = view(box('Speed (km/h)', error='Invalid input'))
```

### Textbox - Password

Set `password=True` when accepting passwords and other confidential inputs.


```py
password = view(box('Password field', password=True))
view(f'Your password `{password}` is not strong enough!')
```

### Textbox - Multiple lines

Set `lines=` to show a multi-line text box (also called a *text area*).


```py
bio = view(box('Bio:', lines=5))
view(f'**Bio:** {bio}')
```


Note that `lines=` only controls the initial height of the textbox, and
multi-line textboxes can be resized by the user.

### Spinbox - Basic

Call `box()` with `mode='number'` to show a box with increment/decrement buttons.
(also called a *spinbox*).


```py
speed = view(box('Speed (km/h)', mode='number'))
view(f'Your speed is {speed} km/h')
```

### Spinbox - Value

Set `value=` to a numeric value to prefill the box with the value.

The mode setting `mode='number'` is implied, and can be elided.


```py
speed = view(box('Speed (km/h)', value=42))
view(f'Your speed is {speed} km/h')
```


In other words, calling `box()` with a numeric `value` has the same effect
as setting `mode='number'`, and is the preferred usage.

### Spinbox - Min

Set `min=` to specify a minimum value.


```py
speed = view(box('Speed (km/h)', min=10))
view(f'Your speed is {speed} km/h')
```

### Spinbox - Max

Set `max=` to specify a maximum value.


```py
speed = view(box('Speed (km/h)', max=100))
view(f'Your speed is {speed} km/h')
```

### Spinbox - Step

Set `step=` to specify how much to increment or decrement by.

The default step is `1`.


```py
speed = view(box('Speed (km/h)', step=5))
view(f'Your speed is {speed} km/h')
```

### Spinbox - Precision

Set `precision=` to specify how many decimal places the value should be rounded to.

The default is calculated based on the precision of step:

- if step = 1, precision = 0
- if step = 0.42, precision = 2
- if step = 0.0042, precision = 4


```py
speed = view(box('Speed (m/s)', value=0.6, min=-2, max=2, step=0.2, precision=2))
view(f'Your speed is {speed} m/s')
```

### Spinbox - Min, Max, Step, Precision

`min=`, `max=`, `step=` and `precision=` can be combined.


```py
speed = view(box('Speed (km/h)', min=10, max=100, step=5))
view(f'Your speed is {speed} km/h')
```

### Spinbox - Range

Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
speed = view(box('Speed (km/h)', range=(10, 100)))
view(f'Your speed is {speed} km/h')
```

### Spinbox - Range with step

Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.

This is a shorthand notation for setting `min=`, `max=` and `step` individually.


```py
speed = view(box('Speed (km/h)', range=(10, 100, 5)))
view(f'Your speed is {speed} km/h')
```

### Spinbox - Range with precision

Setting `range=` to a `(min, max, step, precision)` tuple is a shorthand notation for setting
`min=`, `max=`, `step` and `precision` individually.


```py
speed = view(box('Speed (m/s)', value=0.6, range=(-2, 2, 0.2, 2)))
view(f'Your speed is {speed} m/s')
```

### Spinbox - Zero-crossing range

Ranges can cross zero.


```py
speed = view(box('Speed (m/s)', value=-3, range=(-5, 5)))
view(f'Your speed is {speed} m/s')
```

### Spinbox - Fractional steps

Steps can be fractional.


```py
speed = view(box('Speed (m/s)', value=0.6, range=(-2, 2, 0.2)))
view(f'Your speed is {speed} m/s')
```

### Pickers - Basic

A *picker* is a box that allows the user to pick one or more options from several presented options, like buttons,
checklists, dropdowns, color pickers, and so on.

Set `options=` to create a picker.


```py
choice = view(box('Choose a color', options=[
    'green', 'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```


There are several ways to create options. These are explained in the next section. The simplest way is to supply a
sequence (tuple, set or list) of strings.

By default, this shows buttons for up to 3 options, radio buttons for up to 7 options,
or a dropdown menu for more than 7 options.
This behavior can be controlled using `mode=`, explained in later examples.

The example above has 4 options, hence radio buttons are shown.

### Pickers - Buttons

Buttons are shown for up to 3 options.

Set `mode='button'` to display buttons regardless of the number of options.


```py
choice = view(box('Choose a color', options=[
    'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```

### Pickers - Radio Buttons

Radio buttons is shown for 4-7 options.

Set `mode='radio'` to display radio buttons regardless of the number of options.


```py
choice = view(box('Choose a color', options=[
    'green', 'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```

### Pickers - Dropdown

A dropdown menu is shown for more than 7 options.

Set `mode='menu'` to display a dropdown menu regardless of the number of options.


```py
choice = view(box('Choose a color', options=[
    'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Pickers - Dropdown List

Set `multiple=True` to allow choosing more than one option. The return value is a list of choices made.

By default, this displays checkboxes for up to 7 options, or a dropdown menu for more than 7 options.

Set `mode='menu'` to display a dropdown menu regardless of the number of options.


```py
choices = view(box('Choose some colors', multiple=True, options=[
    'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choices}.')
```

### Pickers - Checklist

A checklist is shown for up to 7 options when `multiple=True`.

Set `mode='check'` to display a checklist regardless of the number of options.


```py
choices = view(box('Choose some colors', mode='check', multiple=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choices}.')
```

### Pickers - Required

Set `required=True` to indicate that input is required.


```py
choice = view(box('Choose a color', mode='menu', required=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Pickers - Error

Set `error=` to show an error message below the box.


```py
choice = view(box('Choose a color', mode='menu', error='Invalid input', options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Options - Basic

An `option` represents one of several choices to be presented to the user.
It's used by all kinds of pickers: buttons, dropdowns, checklists, color pickers, and so on.

An option has a `value` and `text`, created using `option(value, text)`.

- The `value` is the value returned when the user picks that option. It is not user-visible.
- The `text` is typically used as a label for the option.

If `text` is not provided, then the `value` is also used as the `text`.

There are other, more concise ways to specify options, explained in later examples.


```py
choice = view(box('Choose a color', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow'),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```

### Options - From sequence

If `options` is a sequence (tuple, set or list), the elements of the sequence are used as options.


```py
choice = view(box('Choose a color', options=[
    'green', 'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```

### Options - From string

If `options=` is set to a string, each word in the string is used as an option.


```py
choice = view(box('Choose a color', options='green yellow orange red'))
view(f'You chose {choice}.')
```


In other words, `'green yellow orange red'` is a shorthand notation for `['green', 'yellow', 'orange', 'red']`.

### Options - From tuples

`options=` can also be specified as a sequence of `(value, text)` tuples.


```py
choice = view(box('Choose a color', options=[
    ('green', 'Green'),
    ('yellow', 'Yellow'),
    ('orange', 'Orange'),
    ('red', 'Red'),
]))
view(f'You chose {choice}.')
```


Here, `(value, text)` is a shorthand notation for `option(value, text)`.

### Options - From dictionary

`options=` can also be specified as a `dict` of `value: text` entries.


```py
choice = view(box('Choose a color', options=dict(
    green='Green',
    yellow='Yellow',
    orange='Orange',
    red='Red',
)))
view(f'You chose {choice}.')
```


This is the most concise way to pass options where labels differ from values.

### Options - Selected

Set `selected=True` to pre-select an option.

Another way to pre-select an option is to set `value=` on the box, as shown in the next example.


```py
choice = view(box('Choose a color', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```

### Options - Value

Set `value=` on the box to pre-select an option having that value.

Another way to pre-select an option is to set `selected=True` on the option, as shown in the previous example.


```py
choice = view(box('Choose a color', value='yellow', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow'),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```

### Buttons - Basic

Set `mode='button'` to show buttons.

`mode=` can be elided when there are 1-3 options.


```py
choice = view(box('Choose a color', mode='button', options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Buttons - Shorthand

Most often, it doesn't make sense to show a text prompt above a set of buttons.

In such cases, `box(mode='button', options=X)` can be shortened to `box(X)`.

In other words, if the first argument to `box()` is a sequence of options, then `mode='button'` is implied.


```py
choice = view(box(['green', 'yellow', 'orange', 'red']))
view(f'You chose {choice}.')
```


This works when `options` is a sequence (tuple, set, list) or dictionary too. The following forms are equivalent:


```py
choice = view(box([
    option('green', 'Green'),
    option('yellow', 'Yellow'),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))

# Shorter
choice = view(box([
    ('green', 'Green'),
    ('yellow', 'Yellow'),
    ('orange', 'Orange'),
    ('red', 'Red'),
]))

# Shortest
choice = view(box(dict(
    green='Green',
    yellow='Yellow',
    orange='Orange',
    red='Red',
)))
```

### Buttons - Selected

Options marked as `selected` are shown in alternate colors, also called *primary* buttons.

This is useful when you want to emphasize certain actions over others.


```py
choice = view(
    'Updates are available!',
    box([
        option('now', 'Update now', selected=True),
        option('tomorrow', 'Remind me tomorrow'),
        option('never', 'Never update'),
    ])
)
view(f'You chose to update {choice}.')
```

### Buttons - Value

Alternatively, Set `value=` to mark a button as *primary*.


```py
choice = view(
    'Updates are available!',
    box(dict(
        now='Update now',
        tomorrow='Remind me tomorrow',
        never='Never update',
    ), value='now')
)
view(f'You chose to update {choice}.')
```

### Buttons - Values

If `value=` is set to a sequence, all buttons with those values are marked as *primary*.


```py
choice = view(
    'Sign me up!',
    box(dict(
        basic='Basic Plan ($9.99/month)',
        pro='Pro Plan ($14.99/month)',
        none='Not interested',
    ), value=['basic', 'pro'])
)
view(f'You chose {choice}.')
```

### Buttons - Split Buttons

Sub-options inside options are shown as split buttons.


```py
choice = view(
    'Send fresh donuts every day?',
    box([
        option('yes', 'Yes!', selected=True),
        option('no', 'No', options=[
            option('later', 'Remind me later', icon='ChatBot'),
            option('never', "Don't ask me again", icon='MuteChat'),
        ]),
    ])
)
view(f'You chose {choice}.')
```

### Buttons - Primary Split Buttons

Sub-options work for primary buttons, too.


```py
choice = view(
    'Send fresh donuts every day?',
    box([
        option('yes', 'Yes!', selected=True, options=[
            option('later', 'Remind me later', icon='ChatBot'),
            option('never', "Don't ask me again", icon='MuteChat'),
        ]),
        option('no', 'No'),
    ])
)
view(f'You chose {choice}.')
```

### Buttons - Caption

Set `caption=` to describe buttons.


```py
choice = view(
    'Send fresh donuts every day?',
    box([
        option('yes', 'Sign me up!', caption='Terms and conditions apply', selected=True),
        option('no', 'Not now', caption='I will decide later'),
    ])
)
view(f'You chose {choice}.')
```

### Buttons - Layout

By default, buttons are laid out row-wise. Set `row=False` to lay them column-wise.


```py
choice = view(
    'Choose a color:',
    box([
        option('auto', 'Automatic', selected=True),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ], row=False)
)
view(f'You chose {choice}.')
```

### Radio Buttons - Basic

Set `mode='radio'` to show radio buttons.

`mode=` can be elided when there are 4-7 options.


```py
choice = view(box('Choose a color', mode='radio', options=[
    'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Radio Buttons - Value

Set `value=` to pre-select an option having that value.


```py
choice = view(box('Choose a color', mode='radio', value='yellow', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow'),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```

### Radio Buttons - Selected

Set `selected=True` to pre-select an option.


```py
choice = view(box('Choose a color', mode='radio', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```

### Radio Buttons - Icons

Set `icon=` to show graphical options.


```py
choice = view(box('Choose a chart type', mode='radio', options=[
    option('area', 'Area', icon='AreaChart', selected=True),
    option('bar', 'Bar', icon='BarChartHorizontal'),
    option('column', 'Column', icon='BarChartVertical'),
    option('line', 'Line', icon='LineChart'),
    option('scatter', 'Scatter', icon='ScatterChart'),
    option('donut', 'Donut', icon='DonutChart'),
]))
view(f'You chose {choice}.')
```

### Dropdown - Basic

Set `mode='menu'` to show a dropdown menu.

`mode=` can be elided when there are more than 7 options.


```py
choice = view(box('Choose a color', mode='menu', options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Dropdown - Value

Set `value=` to pre-select an option having that value.


```py
choice = view(box('Choose a color', mode='menu', value='yellow', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow'),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```

### Dropdown - Selected

Set `selected=True` to pre-select an option.


```py
choice = view(box('Choose a color', mode='menu', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```

### Dropdown - Grouped

Options can have sub-options. This is useful for grouping options into categories.

`mode=menu` is implied if options are grouped.


```py
choice = view(box('Choose a color', options=[
    option('primary', 'Primary Colors', options=[
        option('red', 'Red'),
        option('blue', 'Blue'),
        option('yellow', 'Yellow'),
    ]),
    option('secondary', 'Secondary Colors', options=[
        option('violet', 'Violet'),
        option('green', 'Green'),
        option('orange', 'Orange'),
    ]),
]))
view(f'You chose {choice}.')
```

### Dropdown - Editable

Set `editable=True` to allow arbitrary input in addition to the presented options.

`mode=menu` is implied if `editable=True`.


```py
choice = view(box('Choose a color', editable=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Dropdown List - Basic

Set `mode='menu'` with `multiple=True` to show a dropdown menu that allows multiple options to be selected.

`mode=` can be elided when there are more than 7 options.


```py
choices = view(box(
    'Choose some colors',
    mode='menu',
    multiple=True,
    options=['green', 'yellow', 'orange', 'red']
))
view(f'You chose {choices}.')
```

### Dropdown List - Value

Set `value=` to pre-select options having those values.


```py
choices = view(box(
    'Choose some colors',
    mode='menu',
    multiple=True,
    value=['yellow', 'red'],
    options=['green', 'yellow', 'orange', 'red']
))
view(f'You chose {choices}.')
```

### Dropdown List - Selected

Alternatively, set `selected=True` to pre-select one or more options.


```py
choices = view(box(
    'Choose some colors',
    mode='menu',
    multiple=True,
    options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red', selected=True),
    ]
))
view(f'You chose {choices}.')
```

### Checklist - Basic

Set `mode='check'` to show a checklist

`mode=` can be elided when there are 1-7 options.


```py
choices = view(box(
    'Choose some colors',
    mode='check',
    multiple=True,
    options=['green', 'yellow', 'orange', 'red']
))
view(f'You chose {choices}.')
```

### Checklist - Value

Set `value=` to pre-select options having those values.


```py
choices = view(box(
    'Choose some colors',
    mode='check',
    multiple=True,
    value=['yellow', 'red'],
    options=['green', 'yellow', 'orange', 'red']
))
view(f'You chose {choices}.')
```

### Checklist - Selected

Alternatively, set `selected=True` to pre-select one or more options.


```py
choices = view(box(
    'Choose some colors',
    mode='check',
    multiple=True,
    options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red', selected=True),
    ]
))
view(f'You chose {choices}.')
```

### Slider - Basic

Set `mode='range'` to show a slider.

The default range is between `0` and `10`.


```py
speed = view(box('Speed (km/h)', mode='range'))
view(f'Your speed is {speed} km/h')
```

### Slider - Value

Set `value=` to default the slider value.


```py
speed = view(box('Speed (km/h)', mode='range', value=5))
view(f'Your speed is {speed} km/h')
```

### Slider - Min

Set `min=` to specify a minimum value.


```py
speed = view(box('Speed (km/h)', mode='range', min=3))
view(f'Your speed is {speed} km/h')
```

### Slider - Max

Set `max=` to specify a maximum value.


```py
speed = view(box('Speed (km/h)', mode='range', max=100))
view(f'Your speed is {speed} km/h')
```

### Slider - Step

Set `step=` to specify how much to increment or decrement by.

The default step is `1`.


```py
speed = view(box('Speed (km/h)', mode='range', step=2))
view(f'Your speed is {speed} km/h')
```

### Slider - Precision

Set `precision=` to specify how many decimal places the value should be rounded to.

The default is calculated based on the precision of step:

- if step = 1, precision = 0
- if step = 0.42, precision = 2
- if step = 0.0042, precision = 4


```py
speed = view(box('Speed (m/s)', mode='range', value=0.6, min=-2, max=2, step=0.2, precision=2))
view(f'Your speed is {speed} m/s')
```

### Slider - Min, Max, Step, Precision

`min=`, `max=`, `step=` and `precision=` can be combined.


```py
speed = view(box('Speed (km/h)', mode='range', min=10, max=100, step=5))
view(f'Your speed is {speed} km/h')
```

### Slider - Range

Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
speed = view(box('Speed (km/h)', mode='range', range=(10, 100)))
view(f'Your speed is {speed} km/h')
```

### Slider - Range with step

Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.

This is a shorthand notation for setting `min=`, `max=` and `step` individually.


```py
speed = view(box('Speed (km/h)', mode='range', range=(10, 100, 5)))
view(f'Your speed is {speed} km/h')
```

### Slider - Range with precision

Setting `range=` to a `(min, max, step, precision)` tuple is a shorthand notation for setting
`min=`, `max=`, `step` and `precision` individually.


```py
speed = view(box('Speed (m/s)', mode='range', value=0.6, range=(-2, 2, 0.2, 2)))
view(f'Your speed is {speed} m/s')
```

### Slider - Zero-crossing range

Ranges can cross zero.


```py
speed = view(box('Speed (m/s)', mode='range', value=-3, range=(-5, 5)))
view(f'Your speed is {speed} m/s')
```

### Slider - Fractional steps

Steps can be fractional.


```py
speed = view(box('Speed (m/s)', mode='range', value=0.6, range=(-2, 2, 0.2)))
view(f'Your speed is {speed} m/s')
```

### Range Slider - Basic

Set `value=` to a `(start, end)` tuple to show a range slider.

The mode setting `mode='range'` is implied, and can be elided.


```py
start, end = view(box('Speed range (km/h)', value=(3, 7)))
view(f'Your speed ranges between {start} and {end} km/h')
```

### Range Slider - Min

Set `min=` to specify a minimum value.


```py
start, end = view(box('Speed range (km/h)', value=(3, 7), min=3))
view(f'Your speed ranges between {start} and {end} km/h')
```

### Range Slider - Max

Set `max=` to specify a maximum value.


```py
start, end = view(box('Speed range (km/h)', value=(30, 70), max=100))
view(f'Your speed ranges between {start} and {end} km/h')
```

### Range Slider - Step

Set `step=` to specify how much to increment or decrement by.

The default step is `1`.


```py
start, end = view(box('Speed range (km/h)', value=(2, 6), step=2))
view(f'Your speed ranges between {start} and {end} km/h')
```

### Range Slider - Precision

Set `precision=` to specify how many decimal places the value should be rounded to.

The default is calculated based on the precision of step:
- if step = 1, precision = 0
- if step = 0.42, precision = 2
- if step = 0.0042, precision = 4


```py
start, end = view(box('Speed range (m/s)', value=(-0.4, 0.4), min=-2, max=2, step=0.2, precision=2))
view(f'Your speed ranges between {start} and {end} m/s')
```

### Range Slider - Min, Max, Step, Precision

`min=`, `max=`, `step=` and `precision=` can be combined.


```py
start, end = view(box('Speed range (km/h)', value=(30, 70), min=10, max=100, step=5))
view(f'Your speed ranges between {start} and {end} km/h')
```

### Range Slider - Range

Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
start, end = view(box('Speed range (km/h)', value=(30, 70), range=(10, 100)))
view(f'Your speed ranges between {start} and {end} km/h')
```

### Range Slider - Range with step

Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.

This is a shorthand notation for setting `min=`, `max=` and `step` individually.


```py
start, end = view(box('Speed range (km/h)', value=(30, 70), range=(10, 100, 5)))
view(f'Your speed ranges between {start} and {end} km/h')
```

### Range Slider - Range with precision

Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.
Setting `range=` to a `(min, max, step, precision)` tuple is a shorthand notation for setting
`min=`, `max=`, `step` and `precision` individually.


```py
start, end = view(box('Speed range (m/s)', value=(-0.4, 0.4), range=(-2, 2, 0.2, 2)))
view(f'Your speed ranges between {start} and {end} m/s')
```

### Range Slider - Zero-crossing range

Ranges can cross zero.


```py
start, end = view(box('Speed range (m/s)', value=(-3, 3), range=(-5, 5)))
view(f'Your speed ranges between {start} and {end} m/s')
```

### Range Slider - Fractional steps

Steps can be fractional.


```py
start, end = view(box('Speed range (m/s)', value=(-0.4, 0.4), range=(-2, 2, 0.2)))
view(f'Your speed ranges between {start} and {end} m/s')
```

### Time Picker - Basic

Set `mode='time'` to show a time picker.


```py
time = view(box('Set alarm for:', mode='time', value='3:04PM'))
view(f'Alarm set for {time}.')
```

### Time Picker - With seconds

Include seconds in the `value` to show a seconds component.


```py
time = view(box('Set alarm for:', mode='time', value='3:04:05PM'))
view(f'Alarm set for {time}.')
```

### Time Picker - Hour only

Exclude minutes and seconds from the `value` to show only the hour component.


```py
time = view(box('Set alarm for:', mode='time', value='3PM'))
view(f'Alarm set for {time}.')
```

### Time Picker - 24-hour clock

Exclude `AM` or `PM` from the `value` to accept input in military time.


```py
time = view(box('Set alarm for:', mode='time', value='15:04'))
view(f'Alarm set for {time}.')
```

### Time Picker - 24-hour clock, with seconds

Include seconds in the `value` to show a seconds component.


```py
time = view(box('Set alarm for:', mode='time', value='15:04:05'))
view(f'Alarm set for {time}.')
```

### Time Picker - 24-hour clock, hour only

Exclude minutes and seconds from the `value` to show only the hour component.


```py
time = view(box('Set alarm for:', mode='time', value='15'))
view(f'Alarm set for {time}.')
```

### Date Picker - Basic

Set `mode='date'` to show a date-picker.


```py
date = view(box('Pick a date', mode='date'))
view(f'You picked {date}.')
```

### Date Picker - Placeholder

Set `placeholder=` to show placeholder text.


```py
date = view(box('Deliver on', mode='date', placeholder='Delivery date'))
view(f'You picked {date}.')
```

### Date Picker - Required

Set `required=True` to indicate that input is required.


```py
date = view(box('Pick a date', mode='date', required=True))
view(f'You picked {date}.')
```

### Date Picker - Value

Set `value=` to pre-select a date.

Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.


```py
date = view(box('Pick a date', mode='date', value='2021-10-10'))
view(f'You picked {date}.')
```

### Date Picker - Min

Set `min=` to specify a minimum date.


```py
date = view(box('Pick a date', mode='date', value='2021-10-10', min='2019-01-01'))
view(f'You picked {date}.')
```

### Date Picker - Max

Set `max=` to specify a maximum date.


```py
date = view(box('Pick a date', mode='date', value='2021-10-10', max='2022-12-31'))
view(f'You picked {date}.')
```

### Date Picker - Min and Max

Set both `min=` and `max=` to restrict selection between two dates.


```py
date = view(box('Pick a date', mode='date', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
view(f'You picked {date}.')
```

### Date Picker - Range

Set `range=` to a `(min, max)` tuple to restrict selection between two dates.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
date = view(box('Pick a date', mode='date', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
view(f'You picked {date}.')
```

### Calendar - Basic

Set `mode='day'` to show a calendar.


```py
date = view(box('Pick a date', mode='day'))
view(f'You picked {date}.')
```

### Calendar - Value

Set `value=` to pre-select a date.

Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.


```py
date = view(box('Pick a date', mode='day', value='2021-10-10'))
view(f'You picked {date}.')
```

### Calendar - Min

Set `min=` to specify a minimum date.


```py
date = view(box('Pick a date', mode='day', value='2021-10-10', min='2019-01-01'))
view(f'You picked {date}.')
```

### Calendar - Max

Set `max=` to specify a maximum date.


```py
date = view(box('Pick a date', mode='day', value='2021-10-10', max='2022-12-31'))
view(f'You picked {date}.')
```

### Calendar - Min and Max

Set both `min=` and `max=` to restrict selection between two dates.


```py
date = view(box('Pick a date', mode='day', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
view(f'You picked {date}.')
```

### Calendar - Range

Set `range=` to a `(min, max)` tuple to restrict selection between two dates.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
date = view(box('Pick a date', mode='day', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
view(f'You picked {date}.')
```

### Week Picker - Basic

Set `mode='week'` to show a week picker.


```py
week = view(box('Pick a week', mode='week'))
view(f'You picked {week}.')
```

### Week Picker - Value

Set `value=` to pre-select a week.

Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.


```py
week = view(box('Pick a week', mode='week', value='2021-10-10'))
view(f'You picked {week}.')
```

### Week Picker - Min

Set `min=` to specify a minimum date.


```py
week = view(box('Pick a week', mode='week', value='2021-10-10', min='2019-01-01'))
view(f'You picked {week}.')
```

### Week Picker - Max

Set `max=` to specify a maximum date.


```py
week = view(box('Pick a week', mode='week', value='2021-10-10', max='2022-12-31'))
view(f'You picked {week}.')
```

### Week Picker - Min and Max

Set both `min=` and `max=` to restrict selection between two dates.


```py
week = view(box('Pick a week', mode='week', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
view(f'You picked {week}.')
```

### Week Picker - Range

Set `range=` to a `(min, max)` tuple to restrict selection between two dates.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
week = view(box('Pick a week', mode='week', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
view(f'You picked {week}.')
```

### Month Picker - Basic

Set `mode='month'` to show a month picker.


```py
month = view(box('Pick a month', mode='month'))
view(f'You picked {month}.')
```

### Month Picker - Value

Set `value=` to pre-select a month.

Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10'))
view(f'You picked {month}.')
```

### Month Picker - Min

Set `min=` to specify a minimum date.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01'))
view(f'You picked {month}.')
```

### Month Picker - Max

Set `max=` to specify a maximum date.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10', max='2022-12-31'))
view(f'You picked {month}.')
```

### Month Picker - Min and Max

Set both `min=` and `max=` to restrict selection between two dates.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
view(f'You picked {month}.')
```

### Month Picker - Range

Set `range=` to a `(min, max)` tuple to restrict selection between two dates.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
view(f'You picked {month}.')
```

### Tag Picker - Basic

Set `mode='tag'` to display a tag picker. `multiple=True` is implied.


```py
tags = view(box(
    'Choose some tags',
    mode='tag',
    options=['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']
))
view(f'You chose {tags}.')
```

### Tag Picker - Value

Set `value=` to pre-select options having those values.


```py
tags = view(box(
    'Choose some tags',
    mode='tag',
    value=['yellow', 'red'],
    options=['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']
))
view(f'You chose {tags}.')
```

### Tag Picker - Selected

Set `selected=True` to pre-select one or more options.


```py
tags = view(box('Choose some tags', mode='tag', options=[
    option('violet', 'Violet'),
    option('indigo', 'Indigo'),
    option('blue', 'Blue'),
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red', selected=True),
]))
view(f'You chose {tags}.')
```

### Color Picker - Basic

Set `mode='color'` to show a color picker.

The return value is a `(r, g, b, a)` tuple,
where `r`, `g`, `b` are integers between 0-255,
and `a` is an integer between 0-100%.


```py
color = view(box('Choose a color', mode='color'))
r, g, b, a = color
view(f'You chose the color `rgba({r}, {g}, {b}, {a}%)`.')
```

### Color Picker - Value

Set `value=` to pre-select a color.

A color value can be:

- `#RRGGBB` e.g. `#ff0033`
- `#RRGGBBAA` e.g. `#ff003388`
- `#RGB` e.g. `#f03` (same as `#ff0033`)
- `#RGBA` e.g. `#f038` (same as `#ff003388`)
- `rgb(R,G,B)` e.g. `rgb(255, 0, 127)` or `rgb(100%, 0%, 50%)`
- `rgba(R,G,B,A)` e.g. `rgb(255, 0, 127, 0.5)` or `rgb(100%, 0%, 50%, 50%)`
- `hsl(H,S,L)` e.g. `hsl(348, 100%, 50%)`
- `hsl(H,S,L,A)` e.g. `hsl(348, 100%, 50%, 0.5)` or `hsl(348, 100%, 50%, 50%)`
- A [named color](https://drafts.csswg.org/css-color-3/#svg-color) e.g. `red`, `green`, `blue`, etc.
- `transparent` (same as `rgba(0,0,0,0)`)

The return value, as in the previous example, is a `(r, g, b, a)` tuple.


```py
color = view(box('Choose a color', mode='color', value='#a241e8'))
view(f'You chose {color}.')
```

### Color Palette - Basic

Set `options=` with `mode='color'` to show a color palette.

The option's `value` must be a valid color in one of the formats described in the previous example.

Unlike the Color Picker, the Color Palette returns the `value` of the chosen option, and not a `(r,g,b,a)` tuple.


```py
color = view(box('Choose a color', mode='color', options=[
    option('#ff0000', 'Red'),
    option('#00ff00', 'Green'),
    option('#0000ff', 'Blue'),
    option('#ffff00', 'Yellow'),
    option('#00ffff', 'Cyan'),
    option('#ff00ff', 'Magenta'),
]))
view(f'You chose {color}.')
```

### Color Palette - Value

Set `value=` to pre-select an option having that color value.


```py
color = view(box('Choose a color', mode='color', value='#0000ff', options=[
    option('#ff0000', 'Red'),
    option('#00ff00', 'Green'),
    option('#0000ff', 'Blue'),
    option('#ffff00', 'Yellow'),
    option('#00ffff', 'Cyan'),
    option('#ff00ff', 'Magenta'),
]))
view(f'You chose {color}.')
```

### Color Palette - Selected

Alternatively, set `selected=True` to pre-select a color in the palette.


```py
color = view(box('Choose a color', mode='color', options=[
    option('#ff0000', 'Red'),
    option('#00ff00', 'Green'),
    option('#0000ff', 'Blue', selected=True),
    option('#ffff00', 'Yellow'),
    option('#00ffff', 'Cyan'),
    option('#ff00ff', 'Magenta'),
]))
view(f'You chose {color}.')
```

### Rating - Basic

Set `mode='rating'` to accept a star-rating.

By default, five stars are displayed.


```py
stars = view(box('Rate your experience', mode='rating'))
view(f'Your rating was {stars} stars.')
```

### Rating - Value

Set `value=` to specify a default value.


```py
stars = view(box('Rate your experience', mode='rating', value=3))
view(f'Your rating was {stars} stars.')
```

### Rating - Min

Set `min=0` to allow zero stars.


```py
stars = view(box('Rate your experience', mode='rating', min=0))
view(f'Your rating was {stars} stars.')
```

### Rating - Max

Set `max=` to increase the number of stars displayed.


```py
stars = view(box('Rate your experience', mode='rating', value=3, max=10))
view(f'Your rating was {stars} stars.')
```

### Rating - Min and max

`min=` and `max=` can be combined.


```py
stars = view(box('Rate your experience', mode='rating', value=3, min=0, max=10))
view(f'Your rating was {stars} stars.')
```

### Rating - Range

Set `range=` to a `(min, max)` tuple to control min/max stars.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
stars = view(box('Rate your experience', mode='rating', value=3, range=(0, 10)))
view(f'Your rating was {stars} stars.')
```
