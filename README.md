# H<sub>2</sub>O Nitro

Nitro (N<sub>2</sub>O) is the quickest way to build web apps using Python. No front-end experience required.

![Nitro](assets/gh-readme-banner.png)

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
    name = view(box('What is your name?'))
    feel = view(box(f'How do you feel today, {name}?'))
    view(f'What a coincidence, {name}, I feel {feel}, too!')
```

## Features

- **No HTML/Javascript.** Build sophisticated multi-page wizard-like workflows and walkthroughs using pure Python.
- **Code.** Laser-focused on keeping application code simple, concise, and clear.
  - **Simplicity.** Page flow follows code flow.
  - **Conciseness.** Lowest lines of code for expressing solutions to a given problem. Less code = less bugs.
  - **Clarity.** Entire apps can be written without jumping through callbacks, request handlers, or event handlers.
- **Batteries-included.** Huge library of sophisticated, accessibility-friendly widgets and data visualizations.
- **Library.** Nitro is a library, not a server. Integrates with Flask, Tornado, Django, Uvicorn and other frameworks.
  Can be integrated into your existing applications.
- **Prototyping-to-production.** Carefully designed API to rapidly prototype new ideas, and progressively improve
  presentation layout and aesthetics over time without affecting initial implementation simplicity, or sacrificing
  control.
- **Unix philosophy.** Tries to do one thing and do it well: display interactive web content. Bring your own web
  app/server of choice and follow their recommendations for hosting, deployment, security, monitoring, metrics and data
  management.

## Differences from H<sub>2</sub>O Wave

**TL;DR:** Use [Wave](https://wave.h2o.ai/) for building visualization-heavy analytical dashboards. For everything else, use Nitro.

- **Deployment.** Nitro is a library, not a server. It's a heavily stripped-down version of [Wave](https://wave.h2o.ai/) 
  with a different, simpler API, designed for integration with existing web frameworks.
- **Content Management.** Wave is capable of storing and broadcasting content and data, making it simple to build
  dashboards without having to deal with data management. Nitro has no such features.
- **API.** Wave's API is *dashboard-oriented*, and has several features that make it easy to develop and deploy
  real-time analytics and dashboards easily. Nitro's API is *page-flow-oriented*, and makes it radically simple to
  author sophisticated workflows and wizards without dealing with callback functions and request handlers.

## Examples

### Basics - Hello World!

The simplest possible app looks like this:


```py
# Print a message.
view('Hello World!')
```


Here, `view()` is comparable to Python's built-in `print()` function,
and prints its arguments to the web page.

### Basics - Format content

Strings passed to `view()` are interpreted as [Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).


```py
view('This is **bold**.')
```

### Basics - Display multiline content

Triple-quote strings to pass multiple lines of markdown.


```py
view('''
The King said, very gravely:
- Begin at the beginning,
- And go on till you come to the end,
- Then stop.
''')
```


Any leading whitespace on each line are automatically ignored.

### Basics - Display items in parallel

Pass multiple items to `view()` to lay them out top to bottom.


```py
view(
    'Begin at the beginning,',
    'And go on till you come to the end,',
    'Then stop.',
)
```

### Basics - Display items in sequence

Call `view()` multiple times to present a sequence of items, one at a time.


```py
view('Begin at the beginning,')
view('And go on till you come to the end,')
view('Then stop.')
```

### Basics - Accept user input

Call `box()` to create an input field.

The `view()` function returns user inputs when it contains one or more input fields.

`box()` creates a textbox by default, but can also create other kinds of input fields, like checkboxes,
dropdowns, spinboxes, etc.


```py
# Display a textbox and assign the entered value to a variable.
x = view(box('What is your name?', value='Boaty McBoatface'))
# Print the entered value.
view(f'Hello, {x}!')
```


Here, `view()` behaves similar to Python's built-in `input()` function.

### Basics - Accept inputs in sequence

Call `view()` multiple times to accept a sequence of inputs, one at a time.


```py
# Prompt for first name.
first_name = view(box('First name', value='Boaty'))
# Prompt for last name.
last_name = view(box('Last name', value='McBoatface'))
# Print the entered values.
view(f'Hello, {first_name} {last_name}!')
```

### Basics - Accept inputs in parallel

Pass multiple items to `view()` to show them together.

The `view()` function returns multiple values if it contains multiple input fields.


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

`view()` and `box()` can be chained together to form sophisticated workflows and wizards.

Building such a multi-page interactive app with plain web frameworks can be
a fairly complex endeavor, weaving together requests and replies with logic spread across
multiple functions or callbacks, but Nitro makes all this delightfully simple!

Note how the example below combines `view()` with conditionals and loops, while keeping the code
simple, concise, and clear.


```py
menu = dict(
    Donut=['Plain', 'Glazed', 'Chocolate'],
    Coffee=['Dark-roast', 'Medium-roast', 'Decaf'],
)

items = view(box(
    'What would you like to order today?',
    options=list(menu.keys()),  # Menu item names.
    multiple=True,  # Allow multiple selections.
))

if len(items) == 0:  # Nothing selected.
    view(f'Nothing to order? Goodbye!')
    return

summary = ''  # The order summary, which we'll display later.
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

### Markdown - Formatting

Markdown blocks support GFM (Github Flavored Markdown).


```py
view('''
# Heading 1
## Heading 2
### Heading 3 
#### Heading 4
##### Heading 5 
###### Small print

This is a paragraph, with **bold**, *italics* (or _italics_), ***important***, `code`
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

### Markdown - Syntax highlighting

Code blocks in Markdown support syntax highlighting.


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

### Markdown - Links

Local links in markdown content behave just like any other input.
Clicking on a local link returns the name of the link.


```py
choice = view('''
- [Apples](#apples)
- [Bananas](#bananas)
- [Cherries](#cherries)
''')
view(f'You clicked on {choice}.')
```

### Layout - Row-wise

Use `row()` to show multiple items along a row, left to right.


```py
view(row(
    'Begin at the beginning,',
    'and go on till you come to the end,',
    'then stop.',
))
```


Passing `row=True` to `view()` produces the same result:


```py
view(
    'Begin at the beginning,',
    'and go on till you come to the end,',
    'then stop.',
    row=True,
)
```

### Textbox - Basic

`box()` without any arguments creates a textbox.
The return value is the text entered into the box.


```py
x = view(box())
view(f'You entered {x}.')
```

### Textbox - Label

Any text passed to `box()` is used as a label.


```py
speed = view(box('Speed'))
view(f'Your speed is {speed} km/h.')
```

### Textbox - Value

Use `value=` to prefill the box with a value.


```py
speed = view(box('Speed (km/h)', value='60'))
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

### Numeric Textbox - Basic

Call `box()` with `mode='number'` to show a box with increment/decrement buttons
(also called a *spinbox*).


```py
speed = view(box('Speed (km/h)', mode='number'))
view(f'Your speed is {speed} km/h')
```

### Numeric Textbox - Value

Set `value=` to a numeric value to prefill the box with the value.

The mode setting `mode='number'` is implied, and can be elided.


```py
speed = view(box('Speed (km/h)', value=42))
view(f'Your speed is {speed} km/h')
```


In other words, calling `box()` with a numeric `value` has the same effect
as setting `mode='number'`, and is the preferred usage.

### Numeric Textbox - Min

Set `min=` to specify a minimum value.


```py
speed = view(box('Speed (km/h)', min=10))
view(f'Your speed is {speed} km/h')
```

### Numeric Textbox - Max

Set `max=` to specify a maximum value.


```py
speed = view(box('Speed (km/h)', max=100))
view(f'Your speed is {speed} km/h')
```

### Numeric Textbox - Step

Set `step=` to specify how much to increment or decrement by.

The default step is `1`.


```py
speed = view(box('Speed (km/h)', step=5))
view(f'Your speed is {speed} km/h')
```

### Numeric Textbox - Precision

Set `precision=` to specify how many decimal places the value should be rounded to.

The default is calculated based on the precision of step:
- if step = 1, precision = 0
- if step = 0.42, precision = 2
- if step = 0.0042, precision = 4


```py
speed = view(box('Speed (m/s)', value=0.6, min=-2, max=2, step=0.2, precision=2))
view(f'Your speed is {speed} m/s')
```

### Numeric Textbox - Min, Max, Step, Precision

`min=`, `max=`, `step=` and `precision=` can be combined.


```py
speed = view(box('Speed (km/h)', min=10, max=100, step=5))
view(f'Your speed is {speed} km/h')
```

### Numeric Textbox - Range

Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
speed = view(box('Speed (km/h)', range=(10, 100)))
view(f'Your speed is {speed} km/h')
```

### Numeric Textbox - Range with step

Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.

This is a shorthand notation for setting `min=`, `max=` and `step` individually.


```py
speed = view(box('Speed (km/h)', range=(10, 100, 5)))
view(f'Your speed is {speed} km/h')
```

### Numeric Textbox - Range with precision

Setting `range=` to a `(min, max, step, precision)` tuple is a shorthand notation for setting
`min=`, `max=`, `step` and `precision` individually.


```py
speed = view(box('Speed (m/s)', value=0.6, range=(-2, 2, 0.2, 2)))
view(f'Your speed is {speed} m/s')
```

### Numeric Textbox - Zero-crossing range

Ranges can cross zero.


```py
speed = view(box('Speed (m/s)', value=-3, range=(-5, 5)))
view(f'Your speed is {speed} m/s')
```

### Numeric Textbox - Fractional steps

Steps can be fractional.


```py
speed = view(box('Speed (m/s)', value=0.6, range=(-2, 2, 0.2)))
view(f'Your speed is {speed} m/s')
```

### Menu - Basic

To show a menu, set `options=` to a sequence of options (a tuple, set or list).

There are several ways to create options. These are explained in the next section.

By default, setting `options=` shows buttons for up to 3 options, radio-buttons for up to 7 options,
or a dropdown menu for more than 7 options.

The example below has 4 options, hence radio-buttons are shown.


```py
choice = view(box('Choose a color', options=[
    'green', 'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```

### Menu - Fewer options

Buttons are shown for up to 3 options.


```py
choice = view(box('Choose a color', options=[
    'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```

### Menu - More options

A dropdown is shown for more than 7 options.


```py
choice = view(box('Choose a color', options=[
    'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Menu - Dropdown

Set `mode='menu'` to force a dropdown menu regardless of the number of options.


```py
choice = view(box('Choose a color', mode='menu', options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Menu - Buttons

Set `mode='button'` to force buttons regardless of the number of options.


```py
choice = view(box('Choose a color', mode='button', options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Menu - Radio-buttons

Set `mode='radio'` to force radio-buttons regardless of the number of options,


```py
choice = view(box('Choose a color', mode='radio', options=[
    'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Menu - Multi-select

Set `multiple=True` to allow choosing more than one option,

By default, this displays checkboxes for up to 7 options, or a dropdown menu for more than 7 options.


```py
choice = view(box('Choose a color', multiple=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Menu - Checkboxes

Set `mode='check'` to force checkboxes regardless of the number of options,


```py
choice = view(box('Choose a color', mode='check', multiple=True, options=[
    'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Menu - Multi-select Dropdown

Set `mode='menu'` to force a multi-select dropdown menu regardless of the number of options.


```py
choice = view(box('Choose a color', mode='menu', multiple=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Menu - Editable

Set `editable=True` to allow arbitrary input in addition to the presented options.

`mode=menu` is implied if `editable=True`.


```py
choice = view(box('Choose a color', editable=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Menu - Multi-select and editable

`multiple=True` and `editable=True` can be combined.


```py
choice = view(box('Choose a color', multiple=True, editable=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Menu - Required

Set `required=True` to indicate that input is required.


```py
choice = view(box('Choose a color', mode='menu', required=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Menu - Error

Set `error=` to show an error message below the box.


```py
choice = view(box('Choose a color', mode='menu', error='Invalid input', options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Options - From sequence

If `options` is a sequence (tuple, set or list), the elements of the sequence are used
as both values and labels.


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

### Options - Labels

Use `option(value, label)` to create options having labels different from their values.

There are other, more concise ways to specify options, explained later.


```py
choice = view(box('Choose a color', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow'),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```

### Options - Labels from tuples

`options=` can also be specified as a sequence of `(value, label)` tuples.


```py
choice = view(box('Choose a color', options=[
    ('green', 'Green'),
    ('yellow', 'Yellow'),
    ('orange', 'Orange'),
    ('red', 'Red'),
]))
view(f'You chose {choice}.')
```


Here, `(value, label)` is a shorthand notation for `option(value, label)`.

### Options - Labels from dictionary

`options=` can also be specified as a `dict` of `value: label` entries.


```py
choice = view(box('Choose a color', options=dict(
    green='Green',
    yellow='Yellow',
    orange='Orange',
    red='Red',
)))
view(f'You chose {choice}.')
```


The above example shows the most concise way to specify options having labels different from their values.

### Options - Selected

Set `selected=True` to pre-select an option.


```py
choice = view(box('Choose a color', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```

### Options - Selected (Dropdown)

```py
choice = view(box('Choose a color', mode='menu', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```

### Options - Selected (Buttons)

Selected buttons are shown in alternate (primary) colors.

This is useful when you want to emphasize certain actions over others.


```py
choice = view(box('Updates are available for your system.', mode='button', options=[
    option('now', 'Update now', selected=True),
    option('tomorrow', 'Remind me tomorrow'),
    option('never', 'Never update'),
]))
view(f'You chose to update {choice}.')
```

### Options - Selected (Radio-buttons)

```py
choice = view(box('Choose a color', mode='radio', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```

### Options - Multiple Selected

Multiple options can be pre-selected if the box supports multiple selections (`multiple=True`).


```py
choice = view(box('Choose a color', multiple=True, options=[
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red', selected=True),
]))
view(f'You chose {choice}.')
```

### Options - Multiple Selected (Checkboxes)

```py
choice = view(box('Choose a color', mode='check', multiple=True, options=[
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red', selected=True),
]))
view(f'You chose {choice}.')
```

### Options - Multiple Selected (Dropdown)

```py
choice = view(box('Choose a color', mode='menu', multiple=True, options=[
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red', selected=True),
]))
view(f'You chose {choice}.')
```

### Options - Icons

Set `icon=` to show graphical options.

Icons are shown only if `mode='radio'`.


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

### Options - Group

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

### Options - Group (Buttons)

Sub-options are shown as split buttons if `mode='button'`.


```py
choice = view(box('Send fresh donuts every day?', mode='button', options=[
    option('yes', 'Yes!', selected=True),
    option('no', 'No', options=[
        option('later', 'Remind me later', icon='ChatBot'),
        option('never', "Don't ask me again", icon='MuteChat'),
    ]),
]))
view(f'You chose {choice}.')
```

### Options - Group selected (Buttons)

Sub-options work on selected (primary) buttons, too.


```py
choice = view(box('Send fresh donuts every day?', mode='button', options=[
    option('yes', 'Yes!', selected=True, options=[
        option('later', 'Remind me later', icon='ChatBot'),
        option('never', "Don't ask me again", icon='MuteChat'),
    ]),
    option('no', 'No'),
]))
view(f'You chose {choice}.')
```

### Options - Caption

Set `caption=` to describe options.

Captions are shown only if `mode='button'`.


```py
choice = view(box('Send fresh donuts every day?', options=[
    option('yes', 'Sign me up!', caption='Terms and conditions apply', selected=True),
    option('no', 'Not now', caption='I will decide later'),
]))
view(f'You chose {choice}.')
```

### Options - Layout

By default, buttons are shown row-wise. Set `row=False` to lay them out column-wise.


```py
choice = view(box('Choose a color', mode='button', row=False, options=[
    option('auto', 'Automatic', selected=True),
    option('yellow', 'Yellow'),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
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

Exclude AM/PM from the `value` to accept input in military time.


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

### Rating - Basic

Set `mode='rating'` to accept a star-rating.

By default, five stars are displayed.


```py
stars = view(box('Rating', mode='rating'))
view(f'Your rating was {stars} stars.')
```

### Rating - Value

Set `value=` to specify a default value.


```py
stars = view(box('Rating with value', mode='rating', value=3))
view(f'Your rating was {stars} stars.')
```

### Rating - Min

Set `min=` to specify a minimum value.


```py
stars = view(box('Rating with zero allowed', mode='rating', min=0))
view(f'Your rating was {stars} stars.')
```

### Rating - Max

Set `max=` to specify a maximum value.


```py
stars = view(box('Rating with max', mode='rating', value=3, max=10))
view(f'Your rating was {stars} stars.')
```

### Rating - Min and max

`min=` and `max=` can be combined.


```py
stars = view(box('Rating with range', mode='rating', value=3, min=0, max=10))
view(f'Your rating was {stars} stars.')
```

### Rating - Range

Set `range=` to a `(min, max)` tuple to control min/max stars.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
stars = view(box('Rating with range', mode='rating', value=3, range=(0, 10)))
view(f'Your rating was {stars} stars.')
```
