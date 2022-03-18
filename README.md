# H<sub>2</sub>O Nitro

Nitro (N<sub>2</sub>O) is the quickest way to build web apps using Python. No front-end experience required.

## Features

- **No HTML/Javascript.** Build sophisticated multi-page wizard-like workflows and walkthroughs using pure Python.
- **Code.** Laser-focused on keeping application code simple, concise, and clear.
    - **Simplicity.** Page flow follows code flow.
    - **Conciseness.** Lowest lines of code for expressing solutions to a given problem. Less code = less bugs.
    - **Clarity.** Entire apps can be written without jumping through callbacks, request handlers, or event handlers.
- **Widgets.** Huge library of sophisticated, accessible input controls and data visualization.
- **Library.** Nitro is a library, not a server. Integrates with Flask, Tornado, Django, Uvicorn and other frameworks.
  Use it in existing applications.
- **Prototyping-to-production.** Carefully designed API to rapidly prototype new ideas, and progressively improve
  presentation layout and aesthetics over time without affecting initial implementation simplicity, or sacrificing
  control.
- **Unix philosophy.** Tries to do one thing and do it well: display interactive web content. Bring your own web
  app/server of choice and follow their recommendations for hosting, deployment, security, monitoring, metrics and data
  management.

## Differences from H<sub>2</sub>O Wave

**TL;DR:** Use Wave for building visualization-heavy analytical dashboards. For everything else, use Nitro.

- **Deployment.** Nitro is a library, not a server. It's a heavily stripped-down version of Wave with a simpler,
  different API, designed for integration with existing web frameworks.
- **Content Management.** Wave is capable of storing and broadcasting content and data, making it simple to build
  dashboards without having to deal with data management. Nitro has no such features.
- **API.** Wave's API is *dashboard-oriented*, and has several features that make it easy to develop and deploy
  real-time analytics and dashboards easily. Nitro's API is *page-flow-oriented*, and makes it radically simple to
  author sophisticated workflows and wizards without dealing with callback functions and request handlers.

## Examples

### Basics - Hello World!

The simplest possible app looks like this:


```py
def hello_world(view: View):
    # Print a message.
    view('Hello World!')
```


Here, `view()` is comparable to Python's built-in `print()` function,
and prints its arguments to the web page.

### Basics - Formatting content

Strings passed to `view()` are interpreted as [Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).


```py
def format_content(view: View):
    view('This is **bold**.')
```

### Basics - Markdown blocks

Triple-quote strings to pass multiple lines of markdown.


```py
def format_multiline_content(view: View):
    view('''
    The King said, very gravely:
    - Begin at the beginning,
    - And go on till you come to the end,
    - Then stop.
    ''')
```


Any leading whitespace on each line are automatically ignored.

### Basics - Multiple content

Pass multiple items to `view()` to display them one below the other, top to bottom.


```py
def display_multiple(view: View):
    view(
        'Begin at the beginning,',
        'And go on till you come to the end,',
        'Then stop.',
    )
```

### Basics - Sequencing views

Call `view()` multiple times to display multiple views in sequence, one after the other.


```py
def sequence_views(view: View):
    view('Begin at the beginning,')
    view('And go on till you come to the end,')
    view('Then stop.')
```

### Basics - Accepting user input

Call `box()` to create an input field.

The `view()` function returns user inputs when it contains one or more input fields.


```py
def accept_input(view: View):
    # Display a textbox and assign the entered value to a variable.
    x = view(box('What is your name?', value='Boaty McBoatface'))
    # Print the entered value.
    view(f'Hello, {x}!')
```


Here, `view()` behaves similar to Python's built-in `input()` function.

### Basics - Sequencing inputs

Capture multiple inputs one after the other by simply calling `view()` mutliple times
and using the return values.


```py
def sequence_inputs(view: View):
    # Prompt for first name.
    first_name = view(box('First name', value='Boaty'))
    # Prompt for last name.
    last_name = view(box('Last name', value='McBoatface'))
    # Print the entered values.
    view(f'Hello, {first_name} {last_name}!')
```

### Basics - Accepting multiple inputs

Pass multiple input fields to `view()` to display them one below the other, top to bottom.

The `view()` function returns multiple values if it contains
multiple input fields.


```py
def accept_multiple_inputs(view: View):
    # Prompt for first and last names.
    first_name, last_name = view(
        box('First name', value='Boaty'),
        box('Last name', value='McBoatface'),
    )
    # Print the entered values
    view(f'Hello, {first_name} {last_name}!')
```

### Basics - Putting it all together

`view()` and `box()` can be chained together to author sophisticated workflows and wizards.

Building such a multi-page interactive app with ordinary web frameworks can be
a fairly complex endeavor weaving together requests and replies with logic spread across
multiple functions or callbacks, but Nitro makes this delightfully simple!

Note how the example below combines `view()` with conditions and loops, while keeping the code
simple, concise, and clear.


```py
def dunk_your_donuts(view: View):
    menu = dict(
        Donut=['Plain', 'Frosted', 'Chocolate'],
        Coffee=['Dark-roast', 'Medium-roast', 'Decaf'],
    )

    items = view(box(
        'What would you like to order today?',
        options=list(menu.keys()),
        multiple=True,
    ))

    summary = ''
    for item in items:
        count = view(box(f'How many orders of {item} would you like?', value=3))
        for i in range(count):
            flavor = view(box(
                f'Pick a flavor for {item} #{i + 1}',
                options=menu[item],
            ))
            summary += f'    1. {flavor} {item}\n'

    view(f'''
    ### Order summary:
    {summary}
    Thank you for your order!
    ''')
```

### Layout - Row-wise

Use `row()` to display multiple items along a row, left to right.


```py
def display_row(view: View):
    view(row(
        'Begin at the beginning,',
        'and go on till you come to the end,',
        'then stop.',
    ))
```


Passing `row=True` to `view()` produces the same result:


```py
def display_row_alt(view: View):
    view(
        'Begin at the beginning,',
        'and go on till you come to the end,',
        'then stop.',
        row=True,
    )
```

### Textbox - Basic textbox

`box()` without any arguments creates a textbox.
The return value is the text entered into the textbox.


```py
def textbox_basic(view: View):
    x = view(box())
    view(f'You entered {x}.')
```

### Textbox - Label

Any text passed to `box()` is used as a label.


```py
def textbox_label(view: View):
    speed = view(box('Speed'))
    view(f'Your speed is {speed} km/s.')
```

### Textbox - Placeholder

Pass `placeholder=` to display placeholder text inside the textbox.


```py
def textbox_placeholder(view: View):
    speed = view(box('Speed', placeholder='0 km/s'))
    view(f'Your speed is {speed} km/s.')
```
