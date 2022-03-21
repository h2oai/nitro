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
# `box()` creates a textbox by default, but can also create other kinds of input fields, like checkboxes,
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
# The `view()` function returns multiple values if it contains multiple input fields.
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

# ## Basic
# `box()` without any arguments creates a textbox.
# The return value is the text entered into the box.
def textbox_basic(view: View):
    x = view(box())
    view(f'You entered {x}.')


# ## Label
# Any text passed to `box()` is used as a label.
def textbox_label(view: View):
    speed = view(box('Speed'))
    view(f'Your speed is {speed} km/h.')


# ## Value
# Use `value=` to prefill the box with a value.
def textbox_value(view: View):
    speed = view(box('Speed (km/h)', value='60'))
    view(f'Your speed is {speed} km/h.')


# ## Placeholder
# Use `placeholder=` to display placeholder text inside the box.
def textbox_placeholder(view: View):
    speed = view(box('Speed', placeholder='0 km/h'))
    view(f'Your speed is {speed} km/h.')


# ## Required
# Set `required=True` to indicate that input is required.
def textbox_required(view: View):
    speed = view(box('Speed (km/h)', required=True))
    view(f'Your speed is {speed} km/h.')


# ## Input Mask
# Set `mask=` to specify an input mask. An input mask is used to format the text field
# for the expected entry.
#
# For example, when someone needs to enter a phone number,
# use an input mask to indicate that three sets of digits should be entered.
def textbox_mask(view: View):
    phone = view(box('Phone', mask='(999) 999 - 9999'))
    view(f'Your phone number is {phone}.')


# To construct the input mask:
# - Use `a` to indicate a letter.
# - Use `9` to indicate a number.
# - Use `*` to indicate a letter or number.
# - Use a backslash to escape any character.

# ## Icon
# Set `icon=` to display an icon at the end of the box.
def textbox_icon(view: View):
    phrase = view(box('Filter results containing:', icon='Filter'))
    view(f'You set a filter on `{phrase}`.')


# ## Prefix
# Set `prefix=` to display a prefix at the start of the box.
def textbox_prefix(view: View):
    website = view(box('Website', prefix='https://', value='example.com'))
    view(f'Your website is https://{website}.')


# ## Suffix
# Set `suffix=` to display a suffix at the end of the box.
def textbox_suffix(view: View):
    website = view(box('Website', suffix='.com', value='example'))
    view(f'Your website is {website}.com.')


# ## Prefix and Suffix
# A textbox can display both a prefix and a suffix at the same time.
def textbox_prefix_suffix(view: View):
    website = view(box('Website', prefix='https://', suffix='.com', value='example'))
    view(f'Your website is https://{website}.com.')


# ## Error
# Set `error=` to display an error message below the box.
def textbox_error(view: View):
    speed = view(box('Speed (km/h)', error='Invalid input'))


# ## Password
# Set `password=True` when accepting passwords and other confidential inputs.
def textbox_password(view: View):
    password = view(box('Password field', password=True))
    view(f'Your password `{password}` is not strong enough!')


# ## Multiple lines
# Set `lines=` to display a multi-line text box (also called a *text area*).
def textarea(view: View):
    bio = view(box('Bio:', lines=5))
    view(f'**Bio:** {bio}')


# Note that `lines=` only controls the initial height of the textbox, and
# multi-line textboxes can be resized by the user.

# # Spinbox

# ## Basic
# Call `box()` with `mode='number'` to display a box with increment/decrement buttons
# (also called a *spinbox*).
def spinbox_basic(view: View):
    speed = view(box('Speed (km/h)', mode='number'))
    view(f'Your speed is {speed} km/h')


# ## Value
# Set `value=` to a numeric value to prefill the box with the value.
#
# The mode setting `mode='number'` is implied, and can be elided.
def spinbox_value(view: View):
    speed = view(box('Speed (km/h)', value=42))
    view(f'Your speed is {speed} km/h')


# In other words, calling `box()` with a numeric `value` has the same effect
# as setting `mode='number'`, and is the preferred usage.

# ## Min
# Set `min=` to specify a minimum value.
def spinbox_min(view: View):
    speed = view(box('Speed (km/h)', min=10))
    view(f'Your speed is {speed} km/h')


# ## Max
# Set `max=` to specify a maximum value.
def spinbox_max(view: View):
    speed = view(box('Speed (km/h)', max=100))
    view(f'Your speed is {speed} km/h')


# ## Step
# Set `step=` to specify how much to increment or decrement by.
#
# The default step is `1`.
def spinbox_step(view: View):
    speed = view(box('Speed (km/h)', step=5))
    view(f'Your speed is {speed} km/h')


# ## Precision
# Set `precision=` to specify how many decimal places the value should be rounded to.
#
# The default is calculated based on the precision of step:
# - if step = 1, precision = 0
# - if step = 42.00, precision = 2
# - if step = 0.0042, precision = 4
def spinbox_precision(view: View):
    speed = view(box('Speed (m/s)', value=0.6, min=-2, max=2, step=0.2, precision=2))
    view(f'Your speed is {speed} m/s')


# ## Min, Max, Step, Precision
# `min=`, `max=`, `step=` and `precision=` can be combined in any which way to restrict input.
def spinbox_range(view: View):
    speed = view(box('Speed (km/h)', min=10, max=100, step=5))
    view(f'Your speed is {speed} km/h')


# ## Range
# Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.
#
# This is a shorthand notation for setting both `min=` and `max=`.
def spinbox_range_alt(view: View):
    speed = view(box('Speed (km/h)', range=(10, 100)))
    view(f'Your speed is {speed} km/h')


# ## Range with step
# Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.
#
# This is a shorthand notation for setting `min=`, `max=` and `step` individually.
def spinbox_range_alt_step(view: View):
    speed = view(box('Speed (km/h)', range=(10, 100, 5)))
    view(f'Your speed is {speed} km/h')


# ## Range with precision
# Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.
# Setting `range=` to a `(min, max, step, precision)` tuple is a shorthand notation for setting
# `min=`, `max=`, `step` and `precision` individually.
def spinbox_range_alt_precision(view: View):
    speed = view(box('Speed (m/s)', value=0.6, range=(-2, 2, 0.2, 2)))
    view(f'Your speed is {speed} m/s')


# ## Zero-crossing range
# Ranges can cross zero.
def spinbox_negative(view: View):
    speed = view(box('Speed (m/s)', value=-3, range=(-5, 5)))
    view(f'Your speed is {speed} m/s')


# ## Fractional steps
# Steps can be fractional.
def spinbox_decimal_step(view: View):
    speed = view(box('Speed (m/s)', value=0.6, range=(-2, 2, 0.2)))
    view(f'Your speed is {speed} m/s')


# # Slider

# ## Basic
# Set `mode='range'` to display a slider.
#
# The default range is between `0` and `10`.
def slider(view: View):
    speed = view(box('Speed (km/h)', mode='range'))
    view(f'Your speed is {speed} km/h')


# ## Value
# Set `value=` to default the slider value.
def slider_value(view: View):
    speed = view(box('Speed (km/h)', mode='range', value=5))
    view(f'Your speed is {speed} km/h')


# ## Min
# Set `min=` to specify a minimum value.
def slider_min(view: View):
    speed = view(box('Speed (km/h)', mode='range', min=3))
    view(f'Your speed is {speed} km/h')


# ## Max
# Set `max=` to specify a maximum value.
def slider_max(view: View):
    speed = view(box('Speed (km/h)', mode='range', max=100))
    view(f'Your speed is {speed} km/h')


# ## Step
# Set `step=` to specify how much to increment or decrement by.
#
# The default step is `1`.
def slider_step(view: View):
    speed = view(box('Speed (km/h)', mode='range', step=2))
    view(f'Your speed is {speed} km/h')


# ## Precision
# Set `precision=` to specify how many decimal places the value should be rounded to.
#
# The default is calculated based on the precision of step:
# - if step = 1, precision = 0
# - if step = 42.00, precision = 2
# - if step = 0.0042, precision = 4
def slider_precision(view: View):
    speed = view(box('Speed (m/s)', mode='range', value=0.6, min=-2, max=2, step=0.2, precision=2))
    view(f'Your speed is {speed} m/s')


# ## Min, Max, Step, Precision
# `min=`, `max=`, `step=` and `precision=` can be combined in any which way to restrict input.
def slider_range(view: View):
    speed = view(box('Speed (km/h)', mode='range', min=10, max=100, step=5))
    view(f'Your speed is {speed} km/h')


# ## Range
# Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.
#
# This is a shorthand notation for setting both `min=` and `max=`.
def slider_range_alt(view: View):
    speed = view(box('Speed (km/h)', mode='range', range=(10, 100)))
    view(f'Your speed is {speed} km/h')


# ## Range with step
# Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.
#
# This is a shorthand notation for setting `min=`, `max=` and `step` individually.
def slider_range_alt_step(view: View):
    speed = view(box('Speed (km/h)', mode='range', range=(10, 100, 5)))
    view(f'Your speed is {speed} km/h')


# ## Range with precision
# Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.
# Setting `range=` to a `(min, max, step, precision)` tuple is a shorthand notation for setting
# `min=`, `max=`, `step` and `precision` individually.
def slider_range_alt_precision(view: View):
    speed = view(box('Speed (m/s)', mode='range', value=0.6, range=(-2, 2, 0.2, 2)))
    view(f'Your speed is {speed} m/s')


# ## Zero-crossing range
# Ranges can cross zero.
def slider_negative(view: View):
    speed = view(box('Speed (m/s)', mode='range', value=-3, range=(-5, 5)))
    view(f'Your speed is {speed} m/s')


# ## Fractional steps
# Steps can be fractional.
def slider_decimal_step(view: View):
    speed = view(box('Speed (m/s)', mode='range', value=0.6, range=(-2, 2, 0.2)))
    view(f'Your speed is {speed} m/s')


# # Range Slider

# ## Basic
# Set `value=` to a `(start, end)` tuple to display a range slider.
#
# The mode setting `mode='range'` is implied, and can be elided.
def range_slider(view: View):
    start, end = view(box('Speed range (km/h)', value=(3, 7)))
    view(f'Your speed ranges between {start} and {end} km/h')
