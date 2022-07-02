# Basics

Take your first steps with Nitro.

## Hello World!

Call `view()` to show something on a page.


```py
view('Hello World!')
```


Here, `view()` is comparable to Python's built-in `print()` function,
and prints its arguments to the web page.


![Screenshot](assets/screenshots/hello_world.png)


## Formatting content

Strings passed to `view()` are interpreted as
[Markdown](https://github.github.com/gfm/)


```py
view('_Less_ `code` means _less_ **bugs**.')
```


![Screenshot](assets/screenshots/format_content.png)


## Show multiline content

Triple-quote strings to pass multiple lines of markdown.


```py
view('''
The King said, very gravely:
- Begin at the beginning,
- And go on till you come to the end,
- Then stop.
''')
```


![Screenshot](assets/screenshots/format_multiline_content.png)


## Show multiple items

Pass multiple arguments to `view()` to lay them out top to bottom.


```py
view(
    'Begin at the beginning,',
    'And go on till you come to the end,',
    'Then stop.',
)
```


![Screenshot](assets/screenshots/display_multiple.png)


## Show multiple items, one at a time

Call `view()` multiple times to show items one at a time.

The following example steps through three different pages.


```py
view('Begin at the beginning,')
view('And go on till you come to the end,')
view('Then stop.')
```


![Screenshot](assets/screenshots/sequence_views.png)


## Style text

To style text, put it in a `box()`, and style the box.

`view(text)` is in fact shorthand for `view(box(text))`.


```py
view(
    box('Hello World!', color='red', border='red'),
    box('Hello World!', color='white', background='red'),
    box('Hello World!', width='50%', background='#eee'),
)
```


In general, `box()` can be used to create all kinds of content, like text blocks, dropdowns,
spinboxes, checklists, buttons, calendars, and so on.


![Screenshot](assets/screenshots/style_text.png)


## Get user input

Call `box()` with `value=` to create an input field and pass it to `view()`.

When a view contains an input field, the `view()` function returns its input value.


```py
# Display a textbox and assign the entered value to a variable.
name = view(box('What is your name?', value='Boaty McBoatface'))
# Print the entered value.
view(f'Hello, {name}!')
```


Here, `view(box())` behaves similar to Python's built-in `input()` function.


![Screenshot](assets/screenshots/get_input.png)


## Get multiple inputs, one at a time

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


![Screenshot](assets/screenshots/sequence_inputs.png)


## Get multiple inputs at once

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


![Screenshot](assets/screenshots/accept_multiple_inputs.png)


## Putting it all together

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
items = view(
    '### What would you like to order today?',
    box(
        'Donuts, coffee, or both?',
        options=list(menu.keys()),  # Menu item names.
        multiple=True,  # Allow multiple selections.
    ),
)

if len(items) == 0:  # Nothing selected.
    view(f'Nothing to order? Goodbye!')
    return

# The order summary, which we'll display later.
summary = ['### Order summary:']

# Prompt for counts and flavors.
for item in items:
    count = view(
        f'### How many orders of {item} would you like?',
        box(f'{item} count', value=3),
    )
    for i in range(count):
        flavor = view(
            f'### Pick a flavor for {item} #{i + 1}',
            box(mode='radio', options=menu[item]),
        )
        summary.append(f'1. {flavor} {item}')

summary.append('\nThank you for your order!')

# Finally, show summary.
view('\n'.join(summary))
```


Building a similar multi-page interactive app with a regular web framework can be
a fairly complex endeavor, weaving together requests and replies with logic spread across
multiple functions , but Nitro makes all this delightfully simple!


![Screenshot](assets/screenshots/dunk_your_donuts.png)
