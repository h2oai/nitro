from h2o_nitro import View, box, row, col


# # Basics

# ## Hello World!
# The simplest possible app looks like this:
def hello_world(view: View):
    # Print a message.
    view('Hello World!')


# Here, `view()` is comparable to Python's built-in `print()` function,
# and prints its arguments to the web page.

# ## Format content
# Strings passed to `view()` are interpreted as [Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).
def format_content(view: View):
    view('This is **bold**.')


# ## Display multiline content
# Triple-quote strings to pass multiple lines of markdown.
def format_multiline_content(view: View):
    view('''
    The King said, very gravely:
    - Begin at the beginning,
    - And go on till you come to the end,
    - Then stop.
    ''')


# Any leading whitespace on each line are automatically ignored.

# ## Display items in parallel
# Pass multiple items to `view()` to lay them out top to bottom.
def display_multiple(view: View):
    view(
        'Begin at the beginning,',
        'And go on till you come to the end,',
        'Then stop.',
    )


# ## Display items in sequence
# Call `view()` multiple times to present a sequence of items, one at a time.
def sequence_views(view: View):
    view('Begin at the beginning,')
    view('And go on till you come to the end,')
    view('Then stop.')


# ## Accept user input
# Call `box()` to create an input field.
#
# The `view()` function returns user inputs when it contains one or more input fields.
#
# `box()` creates a textbox by default, but can also create other kinds of # input fields, like checkboxes,
# dropdowns, spinboxes, etc.
def accept_input(view: View):
    # Display a textbox and assign the entered value to a variable.
    x = view(box('What is your name?', value='Boaty McBoatface'))
    # Print the entered value.
    view(f'Hello, {x}!')


# Here, `view()` behaves similar to Python's built-in `input()` function.

# ## Accept inputs in sequence
# Call `view()` multiple times to accept a sequence of inputs, one at a time.
def sequence_inputs(view: View):
    # Prompt for first name.
    first_name = view(box('First name', value='Boaty'))
    # Prompt for last name.
    last_name = view(box('Last name', value='McBoatface'))
    # Print the entered values.
    view(f'Hello, {first_name} {last_name}!')


# ## Accept inputs in parallel
# Pass multiple items to `view()` to display them together.
#
# The `view()` function returns multiple values if it contains # multiple input fields.
def accept_multiple_inputs(view: View):
    # Prompt for first and last names.
    first_name, last_name = view(
        box('First name', value='Boaty'),
        box('Last name', value='McBoatface'),
    )
    # Print the entered values
    view(f'Hello, {first_name} {last_name}!')


# ## Putting it all together
# `view()` and `box()` can be chained together to form sophisticated workflows and wizards.
#
# Building such a multi-page interactive app with plain web frameworks can be
# a fairly complex endeavor, weaving together requests and replies with logic spread across
# multiple functions or callbacks, but Nitro makes all this delightfully simple!
#
# Note how the example below combines `view()` with conditionals and loops, while keeping the code
# simple, concise, and clear.
def dunk_your_donuts(view: View):
    menu = dict(
        Donut=['Plain', 'Frosted', 'Chocolate'],
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


# # Layout

# ## Row-wise
# Use `row()` to display multiple items along a row, left to right.
def display_row(view: View):
    view(row(
        'Begin at the beginning,',
        'and go on till you come to the end,',
        'then stop.',
    ))


# Passing `row=True` to `view()` produces the same result:
def display_row_alt(view: View):
    view(
        'Begin at the beginning,',
        'and go on till you come to the end,',
        'then stop.',
        row=True,
    )


# # Textbox

# ## Basic textbox
# `box()` without any arguments creates a textbox.
# The return value is the text entered into the textbox.
def textbox_basic(view: View):
    x = view(box())
    view(f'You entered {x}.')


# ## Label
# Any text passed to `box()` is used as a label.
def textbox_label(view: View):
    speed = view(box('Speed'))
    view(f'Your speed is {speed} km/s.')


# ## Placeholder
# Pass `placeholder=` to display placeholder text inside the textbox.
def textbox_placeholder(view: View):
    speed = view(box('Speed', placeholder='0 km/s'))
    view(f'Your speed is {speed} km/s.')
