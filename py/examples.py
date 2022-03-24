from h2o_nitro import View, box, row, col, option


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
# Pass multiple items to `view()` to show them together.
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


# # Markdown

# ## Formatting
# Markdown blocks support GFM (Github Flavored Markdown).
def markdown_basic(view: View):
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


# ## Syntax highlighting
# Code blocks in Markdown support syntax highlighting.
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


# ## Links
# Local links in markdown content behave just like any other input.
# Clicking on a local link returns the name of the link.
def markdown_links(view: View):
    choice = view('''
    - [Apples](#apples)
    - [Bananas](#bananas)
    - [Cherries](#cherries)
    ''')
    view(f'You clicked on {choice}.')


# # Layout

# ## Row-wise
# Use `row()` to show multiple items along a row, left to right.
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
# Use `placeholder=` to show placeholder text inside the box.
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
# For example, to accept a phone number, use an input mask containing three sets of digits.
def textbox_mask(view: View):
    phone = view(box('Phone', mask='(999) 999 - 9999'))
    view(f'Your phone number is {phone}.')


# To construct the input mask:
# - Use `a` to indicate a letter.
# - Use `9` to indicate a number.
# - Use `*` to indicate a letter or number.
# - Use a backslash to escape any character.

# ## Icon
# Set `icon=` to show an icon at the end of the box.
def textbox_icon(view: View):
    phrase = view(box('Filter results containing:', icon='Filter'))
    view(f'You set a filter on `{phrase}`.')


# ## Prefix
# Set `prefix=` to show a prefix at the start of the box.
def textbox_prefix(view: View):
    website = view(box('Website', prefix='https://', value='example.com'))
    view(f'Your website is https://{website}.')


# ## Suffix
# Set `suffix=` to show a suffix at the end of the box.
def textbox_suffix(view: View):
    website = view(box('Website', suffix='.com', value='example'))
    view(f'Your website is {website}.com.')


# ## Prefix and Suffix
# A textbox can show both a prefix and a suffix at the same time.
def textbox_prefix_suffix(view: View):
    website = view(box('Website', prefix='https://', suffix='.com', value='example'))
    view(f'Your website is https://{website}.com.')


# ## Error
# Set `error=` to show an error message below the box.
def textbox_error(view: View):
    speed = view(box('Speed (km/h)', error='Invalid input'))


# ## Password
# Set `password=True` when accepting passwords and other confidential inputs.
def textbox_password(view: View):
    password = view(box('Password field', password=True))
    view(f'Your password `{password}` is not strong enough!')


# ## Multiple lines
# Set `lines=` to show a multi-line text box (also called a *text area*).
def textarea(view: View):
    bio = view(box('Bio:', lines=5))
    view(f'**Bio:** {bio}')


# Note that `lines=` only controls the initial height of the textbox, and
# multi-line textboxes can be resized by the user.

# # Numeric Textbox

# ## Basic
# Call `box()` with `mode='number'` to show a box with increment/decrement buttons
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
# - if step = 0.42, precision = 2
# - if step = 0.0042, precision = 4
def spinbox_precision(view: View):
    speed = view(box('Speed (m/s)', value=0.6, min=-2, max=2, step=0.2, precision=2))
    view(f'Your speed is {speed} m/s')


# ## Min, Max, Step, Precision
# `min=`, `max=`, `step=` and `precision=` can be combined.
def spinbox_range(view: View):
    speed = view(box('Speed (km/h)', min=10, max=100, step=5))
    view(f'Your speed is {speed} km/h')


# ## Range
# Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
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


# # Menu

# ## Basic
# To show a menu, set `options=` to a sequence of options (a tuple, set or list).
#
# There are several ways to create options. These are explained in the next section.
#
# By default, setting `options=` shows buttons for up to 3 options, radio-buttons for up to 7 options,
# or a dropdown menu for more than 7 options.
#
# The example below has 4 options, hence radio-buttons are shown.
def menu_basic(view: View):
    choice = view(box('Choose a color', options=[
        'green', 'yellow', 'orange', 'red'
    ]))
    view(f'You chose {choice}.')


# ## Fewer options
# Buttons are shown for up to 3 options.
#
def menu_short(view: View):
    choice = view(box('Choose a color', options=[
        'yellow', 'orange', 'red'
    ]))
    view(f'You chose {choice}.')


# ## More options
# A dropdown is shown for more than 7 options.
#
def menu_long(view: View):
    choice = view(box('Choose a color', options=[
        'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Dropdown
# Set `mode='menu'` to force a dropdown menu regardless of the number of options.
def menu_dropdown(view: View):
    choice = view(box('Choose a color', mode='menu', options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Buttons
# Set `mode='button'` to force buttons regardless of the number of options.
def menu_buttons(view: View):
    choice = view(box('Choose a color', mode='button', options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Radio-buttons
# Set `mode='radio'` to force radio-buttons regardless of the number of options,
def menu_radio_buttons(view: View):
    choice = view(box('Choose a color', mode='radio', options=[
        'blue', 'green', 'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Multi-select
# Set `multiple=True` to allow choosing more than one option,
#
# By default, this displays checkboxes for up to 7 options, or a dropdown menu for more than 7 options.
def menu_multiple(view: View):
    choice = view(box('Choose a color', multiple=True, options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Checkboxes
# Set `mode='check'` to force checkboxes regardless of the number of options,
def menu_check(view: View):
    choice = view(box('Choose a color', mode='check', multiple=True, options=[
        'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Multi-select Dropdown
# Set `mode='menu'` to force a multi-select dropdown menu regardless of the number of options.
def menu_dropdown_multiple(view: View):
    choice = view(box('Choose a color', mode='menu', multiple=True, options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Editable
# Set `editable=True` to allow arbitrary input in addition to the presented options.
#
# `mode=menu` is implied if `editable=True`.
def menu_editable(view: View):
    choice = view(box('Choose a color', editable=True, options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Multi-select and editable
# `multiple=True` and `editable=True` can be combined.
def menu_multiple_editable(view: View):
    choice = view(box('Choose a color', multiple=True, editable=True, options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Required
# Set `required=True` to indicate that input is required.
def menu_dropdown_required(view: View):
    choice = view(box('Choose a color', mode='menu', required=True, options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Error
# Set `error=` to show an error message below the box.
def menu_dropdown_error(view: View):
    choice = view(box('Choose a color', mode='menu', error='Invalid input', options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# # Options

# ## From sequence
# If `options` is a sequence (tuple, set or list), the elements of the sequence are used
# as both values and labels.

def options_sequence(view: View):
    choice = view(box('Choose a color', options=[
        'green', 'yellow', 'orange', 'red'
    ]))
    view(f'You chose {choice}.')


# ## From string
# If `options=` is set to a string, each word in the string is used as an option.
def options_string(view: View):
    choice = view(box('Choose a color', options='green yellow orange red'))
    view(f'You chose {choice}.')


# In other words, `'green yellow orange red'` is a shorthand notation for `['green', 'yellow', 'orange', 'red']`.


# ## Labels
# Use `option(value, label)` to create options having labels different from their values.
#
# There are other, more concise ways to specify options, explained later.
def options_labels(view: View):
    choice = view(box('Choose a color', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# ## Labels from tuples
# `options=` can also be specified as a sequence of `(value, label)` tuples.
def options_tuples(view: View):
    choice = view(box('Choose a color', options=[
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('orange', 'Orange'),
        ('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# Here, `(value, label)` is a shorthand notation for `option(value, label)`.

# ## Labels from dictionary
# `options=` can also be specified as a `dict` of `value: label` entries.
def options_dict(view: View):
    choice = view(box('Choose a color', options=dict(
        green='Green',
        yellow='Yellow',
        orange='Orange',
        red='Red',
    )))
    view(f'You chose {choice}.')


# The above example shows the most concise way to specify options having labels different from their values.

# ## Selected
# Set `selected=True` to pre-select an option.
def options_selected(view: View):
    choice = view(box('Choose a color', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# ## Selected (Dropdown)
def options_selected_menu(view: View):
    choice = view(box('Choose a color', mode='menu', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# ## Selected (Buttons)
# Selected buttons are shown in alternate (primary) colors.
#
# This is useful when you want to emphasize certain actions over others.
def options_selected_button(view: View):
    choice = view(box('Updates are available for your system.', mode='button', options=[
        option('now', 'Update now', selected=True),
        option('tomorrow', 'Remind me tomorrow'),
        option('never', 'Never update'),
    ]))
    view(f'You chose to update {choice}.')


# ## Selected (Radio-buttons)
def options_selected_radio(view: View):
    choice = view(box('Choose a color', mode='radio', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# ## Multiple Selected
# Multiple options can be pre-selected if the box supports multiple selections (`multiple=True`).
def options_selected_multiple(view: View):
    choice = view(box('Choose a color', multiple=True, options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red', selected=True),
    ]))
    view(f'You chose {choice}.')


# ## Multiple Selected (Checkboxes)
def options_selected_multiple_check(view: View):
    choice = view(box('Choose a color', mode='check', multiple=True, options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red', selected=True),
    ]))
    view(f'You chose {choice}.')


# ## Multiple Selected (Dropdown)
def options_selected_multiple_menu(view: View):
    choice = view(box('Choose a color', mode='menu', multiple=True, options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red', selected=True),
    ]))
    view(f'You chose {choice}.')


# ## Icons
# Set `icon=` to show graphical options.
#
# Icons are shown only if `mode='radio'`.
def options_icon(view: View):
    choice = view(box('Choose a chart type', mode='radio', options=[
        option('area', 'Area', icon='AreaChart', selected=True),
        option('bar', 'Bar', icon='BarChartHorizontal'),
        option('column', 'Column', icon='BarChartVertical'),
        option('line', 'Line', icon='LineChart'),
        option('scatter', 'Scatter', icon='ScatterChart'),
        option('donut', 'Donut', icon='DonutChart'),
    ]))
    view(f'You chose {choice}.')


# ## Group
# Options can have sub-options. This is useful for grouping options into categories.
#
# `mode=menu` is implied if options are grouped.
def options_group(view: View):
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


# ## Group (Buttons)
# Sub-options are shown as split buttons if `mode='button'`.
def options_group_button(view: View):
    choice = view(box('Send fresh donuts every day?', mode='button', options=[
        option('yes', 'Yes!', selected=True),
        option('no', 'No', options=[
            option('later', 'Remind me later', icon='ChatBot'),
            option('never', "Don't ask me again", icon='MuteChat'),
        ]),
    ]))
    view(f'You chose {choice}.')


# ## Group selected (Buttons)
# Sub-options work on selected (primary) buttons, too.
def options_group_selected_button(view: View):
    choice = view(box('Send fresh donuts every day?', mode='button', options=[
        option('yes', 'Yes!', selected=True, options=[
            option('later', 'Remind me later', icon='ChatBot'),
            option('never', "Don't ask me again", icon='MuteChat'),
        ]),
        option('no', 'No'),
    ]))
    view(f'You chose {choice}.')


# ## Caption
# Set `caption=` to describe options.
#
# Captions are shown only if `mode='button'`.
def options_caption(view: View):
    choice = view(box('Send fresh donuts every day?', options=[
        option('yes', 'Sign me up!', caption='Terms and conditions apply', selected=True),
        option('no', 'Not now', caption='I will decide later'),
    ]))
    view(f'You chose {choice}.')


# ## Layout
# By default, buttons are shown row-wise. Set `row=False` to lay them out column-wise.
def options_layout(view: View):
    choice = view(box('Choose a color', mode='button', row=False, options=[
        option('auto', 'Automatic', selected=True),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# # Color

# ## Basic
# Set `mode='color'` to show a color picker.
def color_basic(view: View):
    color = view(box('Choose a color', mode='color'))
    view(f'You chose {color}.')


# ## Value
# Set `value=` to pre-select a color.
def color_value(view: View):
    color = view(box('Choose a color', mode='color', value='#a241e8'))
    view(f'You chose {color}.')


# ## Palette
# Set `options=` to restrict colors to a pre-defined palette.
#
# The option `value` must be a valid color.
def color_palette(view: View):
    color = view(box('Choose a color', mode='color', options=[
        option('#ff0000', 'Red'),
        option('#00ff00', 'Green'),
        option('#0000ff', 'Blue'),
        option('#ffff00', 'Yellow'),
        option('#00ffff', 'Cyan'),
        option('#ff00ff', 'Magenta'),
    ]))
    view(f'You chose {color}.')


# ## Selected
# Set `selected=True` to pre-select a color in the palette.
def color_palette_selected(view: View):
    color = view(box('Choose a color', mode='color', options=[
        option('#ff0000', 'Red'),
        option('#00ff00', 'Green'),
        option('#0000ff', 'Blue', selected=True),
        option('#ffff00', 'Yellow'),
        option('#00ffff', 'Cyan'),
        option('#ff00ff', 'Magenta'),
    ]))
    view(f'You chose {color}.')


# # Slider

# ## Basic
# Set `mode='range'` to show a slider.
#
# The default range is between `0` and `10`.
def slider_basic(view: View):
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
# - if step = 0.42, precision = 2
# - if step = 0.0042, precision = 4
def slider_precision(view: View):
    speed = view(box('Speed (m/s)', mode='range', value=0.6, min=-2, max=2, step=0.2, precision=2))
    view(f'Your speed is {speed} m/s')


# ## Min, Max, Step, Precision
# `min=`, `max=`, `step=` and `precision=` can be combined.
def slider_range(view: View):
    speed = view(box('Speed (km/h)', mode='range', min=10, max=100, step=5))
    view(f'Your speed is {speed} km/h')


# ## Range
# Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
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
# Set `value=` to a `(start, end)` tuple to show a range slider.
#
# The mode setting `mode='range'` is implied, and can be elided.
def range_slider_basic(view: View):
    start, end = view(box('Speed range (km/h)', value=(3, 7)))
    view(f'Your speed ranges between {start} and {end} km/h')


# ## Min
# Set `min=` to specify a minimum value.
def range_slider_min(view: View):
    start, end = view(box('Speed range (km/h)', value=(3, 7), min=3))
    view(f'Your speed ranges between {start} and {end} km/h')


# ## Max
# Set `max=` to specify a maximum value.
def range_slider_max(view: View):
    start, end = view(box('Speed range (km/h)', value=(30, 70), max=100))
    view(f'Your speed ranges between {start} and {end} km/h')


# ## Step
# Set `step=` to specify how much to increment or decrement by.
#
# The default step is `1`.
def range_slider_step(view: View):
    start, end = view(box('Speed range (km/h)', value=(2, 6), step=2))
    view(f'Your speed ranges between {start} and {end} km/h')


# ## Precision
# Set `precision=` to specify how many decimal places the value should be rounded to.
#
# The default is calculated based on the precision of step:
# - if step = 1, precision = 0
# - if step = 0.42, precision = 2
# - if step = 0.0042, precision = 4
def range_slider_precision(view: View):
    start, end = view(box('Speed range (m/s)', value=(-0.4, 0.4), min=-2, max=2, step=0.2, precision=2))
    view(f'Your speed ranges between {start} and {end} m/s')


# ## Min, Max, Step, Precision
# `min=`, `max=`, `step=` and `precision=` can be combined.
def range_slider_range(view: View):
    start, end = view(box('Speed range (km/h)', value=(30, 70), min=10, max=100, step=5))
    view(f'Your speed ranges between {start} and {end} km/h')


# ## Range
# Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def range_slider_range_alt(view: View):
    start, end = view(box('Speed range (km/h)', value=(30, 70), range=(10, 100)))
    view(f'Your speed ranges between {start} and {end} km/h')


# ## Range with step
# Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.
#
# This is a shorthand notation for setting `min=`, `max=` and `step` individually.
def range_slider_range_alt_step(view: View):
    start, end = view(box('Speed range (km/h)', value=(30, 70), range=(10, 100, 5)))
    view(f'Your speed ranges between {start} and {end} km/h')


# ## Range with precision
# Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.
# Setting `range=` to a `(min, max, step, precision)` tuple is a shorthand notation for setting
# `min=`, `max=`, `step` and `precision` individually.
def range_slider_range_alt_precision(view: View):
    start, end = view(box('Speed range (m/s)', value=(-0.4, 0.4), range=(-2, 2, 0.2, 2)))
    view(f'Your speed ranges between {start} and {end} m/s')


# ## Zero-crossing range
# Ranges can cross zero.
def range_slider_negative(view: View):
    start, end = view(box('Speed range (m/s)', value=(-3, 3), range=(-5, 5)))
    view(f'Your speed ranges between {start} and {end} m/s')


# ## Fractional steps
# Steps can be fractional.
def range_slider_decimal_step(view: View):
    start, end = view(box('Speed range (m/s)', value=(-0.4, 0.4), range=(-2, 2, 0.2)))
    view(f'Your speed ranges between {start} and {end} m/s')


# # Time Picker

# ## Basic
# Set `mode='time'` to show a time picker.
def time_basic(view: View):
    time = view(box('Set alarm for:', mode='time', value='3:04PM'))
    view(f'Alarm set for {time}.')


# ## With seconds
# Include seconds in the `value` to show a seconds component.
def time_seconds(view: View):
    time = view(box('Set alarm for:', mode='time', value='3:04:05PM'))
    view(f'Alarm set for {time}.')


# ## Hour only
# Exclude minutes and seconds from the `value` to show only the hour component.
def time_hour(view: View):
    time = view(box('Set alarm for:', mode='time', value='3PM'))
    view(f'Alarm set for {time}.')


# ## 24-hour clock
# Exclude AM/PM from the `value` to accept input in military time.
def time_24(view: View):
    time = view(box('Set alarm for:', mode='time', value='15:04'))
    view(f'Alarm set for {time}.')


# ## 24-hour clock, with seconds
# Include seconds in the `value` to show a seconds component.
def time_24_seconds(view: View):
    time = view(box('Set alarm for:', mode='time', value='15:04:05'))
    view(f'Alarm set for {time}.')


# ## 24-hour clock, hour only
# Exclude minutes and seconds from the `value` to show only the hour component.
def time_24_hour(view: View):
    time = view(box('Set alarm for:', mode='time', value='15'))
    view(f'Alarm set for {time}.')


# # Date Picker
# ## Basic
# Set `mode='date'` to show a date-picker.
def date_basic(view: View):
    date = view(box('Pick a date', mode='date'))
    view(f'You picked {date}.')


# ## Placeholder
# Set `placeholder=` to show placeholder text.
def date_placeholder(view: View):
    date = view(box('Deliver on', mode='date', placeholder='Delivery date'))
    view(f'You picked {date}.')


# ## Required
# Set `required=True` to indicate that input is required.
def date_required(view: View):
    date = view(box('Pick a date', mode='date', required=True))
    view(f'You picked {date}.')


# ## Value
# Set `value=` to pre-select a date.
def date_value(view: View):
    date = view(box('Pick a date', mode='date', value='2021-10-10'))
    view(f'You picked {date}.')


# ## Min
# Set `min=` to specify a minimum date.
def date_min(view: View):
    date = view(box('Pick a date', mode='date', value='2021-10-10', min='2019-01-01'))
    view(f'You picked {date}.')


# ## Max
# Set `max=` to specify a maximum date.
def date_max(view: View):
    date = view(box('Pick a date', mode='date', value='2021-10-10', max='2022-12-31'))
    view(f'You picked {date}.')


# ## Min and Max
# Set both `min=` and `max=` to restrict selection between two dates.
def date_min_max(view: View):
    date = view(box('Pick a date', mode='date', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
    view(f'You picked {date}.')


# ## Range
# Set `range=` to a `(min, max)` tuple to restrict selection between two dates.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def date_range(view: View):
    date = view(box('Pick a date', mode='date', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    view(f'You picked {date}.')


# # Calendar

# ## Basic
# Set `mode='day'` to show a calendar.
def day_basic(view: View):
    date = view(box('Pick a date', mode='day'))
    view(f'You picked {date}.')


# ## Value
# Set `value=` to pre-select a date.
#
# Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
# Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.
def day_value(view: View):
    date = view(box('Pick a date', mode='day', value='2021-10-10'))
    view(f'You picked {date}.')


# ## Min
# Set `min=` to specify a minimum date.
def day_min(view: View):
    date = view(box('Pick a date', mode='day', value='2021-10-10', min='2019-01-01'))
    view(f'You picked {date}.')


# ## Max
# Set `max=` to specify a maximum date.
def day_max(view: View):
    date = view(box('Pick a date', mode='day', value='2021-10-10', max='2022-12-31'))
    view(f'You picked {date}.')


# ## Min and Max
# Set both `min=` and `max=` to restrict selection between two dates.
def day_min_max(view: View):
    date = view(box('Pick a date', mode='day', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
    view(f'You picked {date}.')


# ## Range
# Set `range=` to a `(min, max)` tuple to restrict selection between two dates.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def day_range(view: View):
    date = view(box('Pick a date', mode='day', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    view(f'You picked {date}.')


# # Week Picker

# ## Basic
# Set `mode='week'` to show a week picker.
def week_basic(view: View):
    week = view(box('Pick a week', mode='week'))
    view(f'You picked {week}.')


# ## Value
# Set `value=` to pre-select a week.
def week_value(view: View):
    week = view(box('Pick a week', mode='week', value='2021-10-10'))
    view(f'You picked {week}.')


# ## Min
# Set `min=` to specify a minimum date.
def week_min(view: View):
    week = view(box('Pick a week', mode='week', value='2021-10-10', min='2019-01-01'))
    view(f'You picked {week}.')


# ## Max
# Set `max=` to specify a maximum date.
def week_max(view: View):
    week = view(box('Pick a week', mode='week', value='2021-10-10', max='2022-12-31'))
    view(f'You picked {week}.')


# ## Min and Max
# Set both `min=` and `max=` to restrict selection between two dates.
def week_min_max(view: View):
    week = view(box('Pick a week', mode='week', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
    view(f'You picked {week}.')


# ## Range
# Set `range=` to a `(min, max)` tuple to restrict selection between two dates.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def week_range(view: View):
    week = view(box('Pick a week', mode='week', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    view(f'You picked {week}.')


# # Month Picker

# ## Basic
# Set `mode='month'` to show a month picker.
def month_basic(view: View):
    month = view(box('Pick a month', mode='month'))
    view(f'You picked {month}.')


# ## Value
# Set `value=` to pre-select a month.
def month_value(view: View):
    month = view(box('Pick a month', mode='month', value='2021-10-10'))
    view(f'You picked {month}.')


# ## Min
# Set `min=` to specify a minimum date.
def month_min(view: View):
    month = view(box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01'))
    view(f'You picked {month}.')


# ## Max
# Set `max=` to specify a maximum date.
def month_max(view: View):
    month = view(box('Pick a month', mode='month', value='2021-10-10', max='2022-12-31'))
    view(f'You picked {month}.')


# ## Min and Max
# Set both `min=` and `max=` to restrict selection between two dates.
def month_min_max(view: View):
    month = view(box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
    view(f'You picked {month}.')


# ## Range
# Set `range=` to a `(min, max)` tuple to restrict selection between two dates.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def month_range(view: View):
    month = view(box('Pick a month', mode='month', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    view(f'You picked {month}.')


# # Rating

# ## Basic
# Set `mode='rating'` to accept a star-rating.
#
# By default, five stars are displayed.
def rating_basic(view: View):
    stars = view(box('Rating', mode='rating'))
    view(f'Your rating was {stars} stars.')


# ## Value
# Set `value=` to specify a default value.
def rating_value(view: View):
    stars = view(box('Rating with value', mode='rating', value=3))
    view(f'Your rating was {stars} stars.')


# ## Min
# Set `min=` to specify a minimum value.
def rating_min(view: View):
    stars = view(box('Rating with zero allowed', mode='rating', min=0))
    view(f'Your rating was {stars} stars.')


# ## Max
# Set `max=` to specify a maximum value.
def rating_max(view: View):
    stars = view(box('Rating with max', mode='rating', value=3, max=10))
    view(f'Your rating was {stars} stars.')


# ## Min and max
# `min=` and `max=` can be combined.
def rating_min_max(view: View):
    stars = view(box('Rating with range', mode='rating', value=3, min=0, max=10))
    view(f'Your rating was {stars} stars.')


# ## Range
# Set `range=` to a `(min, max)` tuple to control min/max stars.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def rating_range(view: View):
    stars = view(box('Rating with range', mode='rating', value=3, range=(0, 10)))
    view(f'Your rating was {stars} stars.')
