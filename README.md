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
- **Minimal API** Just three core functions: `view()`, `box()`, `option()`, and optionally `row()`/`column()` for layout.
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

### Basics - Formatting

Strings passed to `view()` are interpreted as [Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).


```py
view('_Less_ `code` means _less_ **bugs**.')
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

summary = ['### Order summary:']  # The order summary, which we'll display later.

# Pick flavors for each item.
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

### Markdown - Syntax

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

### Markdown - Links as inputs

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

### Layout - Rows

Use `row()` to lay out multiple items along a row, left to right.


```py
view(row(
    'Begin at the beginning,',
    'and go on till you come to the end,',
    'then stop.',
))
```


Setting `row=True` produces the same result as wrapping items with `row()`.


```py
view(
    'Begin at the beginning,',
    'and go on till you come to the end,',
    'then stop.',
    row=True,
)
```

### Layout - Columns

Use `col()` to lay out multiple items along a column, top to bottom.

The example shows one row split into three columns containing three rows each.


```py
view(
    row(
        col(
            '(1, 1)',
            '(1, 2)',
            '(1, 3)',
        ),
        col(
            '(2, 1)',
            '(2, 2)',
            '(2, 3)',
        ),
        col(
            '(3, 1)',
            '(3, 2)',
            '(3, 3)',
        ),
    ),
)
```

### Layout - Form, vertical

Text/markdown and inputs created with `box()` are laid out the same way.

By default, items are laid out top to bottom.


```py
view(
    box('Username', placeholder='someone@company.com'),
    box('Password', password=True),
    box(['Login']),
)
```

### Layout - Form, horizontal

Wrap items with `row()` to lay them out left to right.


```py
view(
    row(
        box('Username', placeholder='someone@company.com'),
        box('Password', password=True),
        box(['Login']),
    )
)
```

### Layout - Form, combined

Use `row()` and `col()` to mix and match how items are laid out.


```py
view(
    row(box('First name'), box('Last name')),
    box('Address line 1'),
    box('Address line 2'),
    row(box('City'), box('State'), box('Zip')),
    box([
        option('yes', 'Sign me up!', selected=True),
        option('no', 'Not now'),
    ])
)
```

### Layout - Form, improved

Specify additional layout parameters like `width=`, `grow=`, etc. to get more control over
how items are laid out.


```py
view(
    row(box('First name'), box('M.I.', width='10%'), box('Last name')),
    box('Address line 1'),
    box('Address line 2'),
    row(box('City', grow=5), box('State', width='20%'), box('Zip', grow=1)),
    box([
        option('yes', 'Sign me up!', caption='Terms and conditions apply', selected=True),
        option('no', 'Not now', caption="I'll decide later"),
    ])
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

### Pickers - Basic

A *picker* is a box that allows the user to pick one or more options from several presented options, like buttons,
checklists, dropdowns, color pickers, and so on.

Set `options=` to create a picker.

There are several ways to create options. These are explained in the next section. The simplest way is to supply a
sequence (tuple, set or list) of strings.

By default, this shows buttons for up to 3 options, radio-buttons for up to 7 options,
or a dropdown menu for more than 7 options.
This behavior can be controlled using `mode=`, explained in later examples.

The example below has 4 options, hence radio-buttons are shown.


```py
choice = view(box('Choose a color', options=[
    'green', 'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```



### Pickers - Radio-buttons

Radio-buttons are shown for 4-7 options.

Set `mode='radio'` to display buttons regardless of the number of options.


```py
choice = view(box('Choose a color', options=[
    'green', 'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```

### Pickers - Buttons

Buttons are shown for up to 3 options.

Set `mode='button'` to display buttons regardless of the number of options.


```py
choice = view(box('Choose a color', options=[
    'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```

### Pickers - Dropdown

A dropdown is shown for more than 7 options.

Set `mode='menu'` to display a dropdown menu regardless of the number of options.


```py
choice = view(box('Choose a color', options=[
    'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Pickers - Checklist

Set `multiple=True` to allow choosing more than one option. The return value is a list of choices made.

By default, this displays checkboxes for up to 7 options, or a dropdown menu for more than 7 options.

Set `mode='check'` to display a checklist regardless of the number of options.


```py
choices = view(box('Choose some colors', multiple=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choices}.')
```

### Pickers - Multi-select Dropdown

Set `multiple=True` to allow choosing more than one option. The return value is a list of choices made.

By default, this displays checkboxes for up to 7 options, or a dropdown menu for more than 7 options.

Set `mode='menu'` to display a dropdown menu regardless of the number of options.


```py
choices = view(box('Choose some colors', multiple=True, options=[
    'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choices}.')
```

### Pickers - Editable Dropdown

Set `editable=True` to allow arbitrary input in addition to the presented options.

`mode=menu` is implied if `editable=True`.


```py
choice = view(box('Choose a color', editable=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
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
It's used by all pickers: buttons, dropdowns, checklists, color pickers, and so on.

An option has a `value` and `text`, created using `option(value, text)`.
- The `value` is the value returned when the user picks that option. It is not user-visible.
- The `text` is user-visible, and is typically used as a label for the option.

If `text` is not provided, then the `value` is also used as the `text`.

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


The above example shows the most concise way to specify options having labels different from their values.

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

### Radio-buttons - Basic

Set `mode='radio'` to show radio-buttons.

`mode=` can be elided when there are 4-7 options.


```py
choice = view(box('Choose a color', mode='radio', options=[
    'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```

### Radio-buttons - Value

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

### Radio-buttons - Selected

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

### Radio-buttons - Icons

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

Most often, it doesn't make sense to show a text prompt for a set of buttons.
In such cases, `box(text=None, options=[a, b, c])` can be shortened to `box([a, b, c])`.

In other words, `box()` can accept options instead of text as its first argument,
and `mode='button'` is implied.


```py
choice = view(box(['green', 'yellow', 'orange', 'red']))
view(f'You chose {choice}.')
```

### Buttons - Selected

Options marked as `selected` are shown in alternate colors, also called *primary* buttons.

This is useful when you want to emphasize certain actions over others.


```py
choice = view(box('Updates are available.', mode='button', options=[
    option('now', 'Update now', selected=True),
    option('tomorrow', 'Remind me tomorrow'),
    option('never', 'Never update'),
]))
view(f'You chose to update {choice}.')
```

### Buttons - Value

Set `value=` to pre-select an option having that value.

This is useful when you want to emphasize certain actions over others.


```py
choice = view(box('Updates are available.', mode='button', value='now', options=[
    option('now', 'Update now'),
    option('tomorrow', 'Remind me tomorrow'),
    option('never', 'Never update'),
]))
view(f'You chose to update {choice}.')
```

### Buttons - Split Buttons

Options can have sub-options. Sub-options are shown as split buttons.


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

### Buttons - Primary Split Buttons

Sub-options work on selected options, too, and are shown in alternate colors.


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

### Buttons - Caption

Set `caption=` to describe options.

Captions are shown only if `mode='button'`.


```py
choice = view(box('Send fresh donuts every day?', options=[
    option('yes', 'Sign me up!', caption='Terms and conditions apply', selected=True),
    option('no', 'Not now', caption='I will decide later'),
]))
view(f'You chose {choice}.')
```

### Buttons - Layout

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

### Checklist - Basic

Set `mode='check'` to show a checklist

`mode=` can be elided when there are 1-7 options.


```py
choices = view(box('Choose some colors', mode='check', multiple=True, options=[
    'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choices}.')
```

### Checklist - Value

Set `value=` to pre-select an option having that value.


```py
choices = view(box('Choose some colors', mode='check', multiple=True, value=['yellow', 'red'], options=[
    option('green', 'Green'),
    option('yellow', 'Yellow'),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choices}.')
```

### Checklist - Selected

Set `selected=True` to pre-select one or more options.


```py
choices = view(box('Choose some colors', mode='check', multiple=True, options=[
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red', selected=True),
]))
view(f'You chose {choices}.')
```

### Multi-select Dropdown - Basic

Set `mode='menu'` with `multiple=True` to show a multi-select dropdown menu.

`mode=` can be elided when there are more than 7 options.


```py
choices = view(box('Choose some colors', mode='menu', multiple=True, options=[
    'green', 'yellow', 'orange', 'red'
]))
view(f'You chose {choices}.')
```

### Multi-select Dropdown - Value

Set `value=` to pre-select an option having that value.


```py
choices = view(box('Choose some colors', mode='menu', multiple=True, value=['yellow', 'red'], options=[
    option('green', 'Green'),
    option('yellow', 'Yellow'),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choices}.')
```

### Multi-select Dropdown - Selected

Set `selected=True` to pre-select one or more options.


```py
choices = view(box('Choose some colors', mode='menu', multiple=True, options=[
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red', selected=True),
]))
view(f'You chose {choices}.')
```

### Tag Picker - Basic

Set `mode='tag'` to display a tag picker. `multiple=True` is implied.


```py
tags = view(box('Choose some tags', mode='tag', options=[
    'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red'
]))
view(f'You chose {tags}.')
```

### Tag Picker - Value

Set `value=` to pre-select an option having that value.


```py
tags = view(box('Choose some tags', mode='tag', value=['yellow', 'red'], options=[
    'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red'
]))
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

### Color Picker - Palette

Set `options=` to restrict colors to a pre-defined palette.

The option's `value` must be a valid color in one of the formats described in the previous example.


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

### Color Picker - Selected

Set `selected=True` to pre-select a color in the palette.


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
