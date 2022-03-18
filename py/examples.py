from h2o_nitro import View, box, row, col


# # Basics

# ## Hello World!
# The simplest possible app looks like this:
def hello_world(view: View):
    # Print a message
    view('Hello World!')


# Here, `view()` is comparable to Python's built-in `print()` function,
# and prints its arguments to the web page.

# ## Formatting content
# Strings passed to `view()` are interpreted as [Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).
def format_content(view: View):
    view('This is **bold**.')


# ## Markdown blocks
# Triple-quote strings to pass multiple lines of markdown.
def format_multiline_content(view: View):
    view('''
    The King said, very gravely:
    - Begin at the beginning,
    - And go on till you come to the end,
    - Then stop.
    ''')


# Any leading whitespace on each line are automatically ignored.

# ## Multiple content
# Pass multiple items to `view()` to display them one below the other, top to bottom.
def display_multiple(view: View):
    view(
        'Begin at the beginning,',
        'And go on till you come to the end,',
        'Then stop.',
    )


# ## Row-wise
# Use `row()` to display multiple items on the same row, left to right.
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


# ## Sequencing views
# To display multiple views in sequence, call `view()` multiple times.
def display_in_sequence(view: View):
    view('Begin at the beginning,')
    view('And go on till you come to the end,')
    view('Then stop.')


# Here, `view()` prints its arguments to the web page.
# The `view()` is comparable to Python's built-in `input()` function.

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
