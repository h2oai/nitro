from h2o_nitro import web_directory, View, box, option, row, col, ContextSwitchError
import simple_websocket
from flask import Flask, request, send_from_directory


hello_world_docs = (
"""
## Basics - Hello World!
Call `view()` to show something on a page.
```py
view('Hello World!')
```
Here, `view()` is comparable to Python's built-in `print()` function,
and prints its arguments to the web page.
""",
    '### Output',
)


def hello_world(view: View):
    view(*hello_world_docs, 'Hello World!')


format_content_docs = (
"""
## Basics - Formatting content
Strings passed to `view()` are interpreted as
[Markdown](https://github.github.com/gfm/)
```py
view('_Less_ `code` means _less_ **bugs**.')
```
""",
    '### Output',
)


def format_content(view: View):
    view(*format_content_docs, '_Less_ `code` means _less_ **bugs**.')


format_multiline_content_docs = (
"""
## Basics - Show multiline content
Triple-quote strings to pass multiple lines of markdown.
```py
view('''
The King said, very gravely:
- Begin at the beginning,
- And go on till you come to the end,
- Then stop.
''')
```
""",
    '### Output',
)


def format_multiline_content(view: View):
    view(*format_multiline_content_docs, '''
    The King said, very gravely:
    - Begin at the beginning,
    - And go on till you come to the end,
    - Then stop.
    ''')


display_multiple_docs = (
"""
## Basics - Show items at once
Pass multiple arguments to `view()` to lay them out top to bottom.
```py
view(
    'Begin at the beginning,',
    'And go on till you come to the end,',
    'Then stop.',
)
```
""",
    '### Output',
)


def display_multiple(view: View):
    view(*display_multiple_docs, 
        'Begin at the beginning,',
        'And go on till you come to the end,',
        'Then stop.',
    )


sequence_views_docs = (
"""
## Basics - Show items one at a time
Call `view()` multiple times to show items one at a time.

The following example steps through three different pages.
```py
view('Begin at the beginning,')
view('And go on till you come to the end,')
view('Then stop.')
```
""",
    '### Output',
)


def sequence_views(view: View):
    view(*sequence_views_docs, 'Begin at the beginning,')
    view(*sequence_views_docs, 'And go on till you come to the end,')
    view(*sequence_views_docs, 'Then stop.')


get_input_docs = (
"""
## Basics - Get user input
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
""",
    '### Output',
)


def get_input(view: View):
    # Display a textbox and assign the entered value to a variable.
    name = view(*get_input_docs, box('What is your name?', value='Boaty McBoatface'))
    # Print the entered value.
    view(*get_input_docs, f'Hello, {name}!')


sequence_inputs_docs = (
"""
## Basics - Get inputs one at a time
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
""",
    '### Output',
)


def sequence_inputs(view: View):
    # Prompt for first name.
    first_name = view(*sequence_inputs_docs, box('First name', value='Boaty'))
    # Prompt for last name.
    last_name = view(*sequence_inputs_docs, box('Last name', value='McBoatface'))
    # Print the entered values.
    view(*sequence_inputs_docs, f'Hello, {first_name} {last_name}!')


accept_multiple_inputs_docs = (
"""
## Basics - Get inputs at once
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
""",
    '### Output',
)


def accept_multiple_inputs(view: View):
    # Prompt for first and last names.
    first_name, last_name = view(*accept_multiple_inputs_docs, 
        box('First name', value='Boaty'),
        box('Last name', value='McBoatface'),
    )
    # Print the entered values
    view(*accept_multiple_inputs_docs, f'Hello, {first_name} {last_name}!')


dunk_your_donuts_docs = (
"""
## Basics - Putting it all together
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
""",
    '### Output',
)


def dunk_your_donuts(view: View):
    # Our menu.
    menu = dict(
        Donut=['Plain', 'Glazed', 'Chocolate'],
        Coffee=['Dark-roast', 'Medium-roast', 'Decaf'],
    )

    # Prompt for items.
    items = view(*dunk_your_donuts_docs, box(
        'What would you like to order today?',
        options=list(menu.keys()),  # Menu item names.
        multiple=True,  # Allow multiple selections.
    ))

    if len(items) == 0:  # Nothing selected.
        view(*dunk_your_donuts_docs, f'Nothing to order? Goodbye!')
        return

    # The order summary, which we'll display later.
    summary = ['### Order summary:']

    # Prompt for counts and flavors.
    for item in items:
        count = view(*dunk_your_donuts_docs, box(f'How many orders of {item} would you like?', value=3))
        for i in range(count):
            flavor = view(*dunk_your_donuts_docs, box(
                f'Pick a flavor for {item} #{i + 1}',
                options=menu[item],
            ))
            summary.append(f'1. {flavor} {item}')

    summary.append('\nThank you for your order!')

    # Finally, show summary.
    view(*dunk_your_donuts_docs, '\n'.join(summary))


markdown_basic_docs = (
"""
## Markdown - Basics
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
""",
    '### Output',
)


def markdown_basic(view: View):
    view(*markdown_basic_docs, '''
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


markdown_links_docs = (
"""
## Markdown - Links as inputs
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
""",
    '### Output',
)


def markdown_links(view: View):
    choice = view(*markdown_links_docs, '''
    Pick a flavor:
    - [Vanilla](#vanilla)
    - [Strawberry](#strawberry)
    - [Chocolate](#chocolate)

    Or, [surprise me](#surprise-me)!
    ''')
    view(*markdown_links_docs, f'You clicked on {choice}.')


markdown_syntax_highlighting_docs = (
"""
## Markdown - Syntax highlighting
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
""",
    '### Output',
)


def markdown_syntax_highlighting(view: View):
    view(*markdown_syntax_highlighting_docs, '''
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


layout_basic_docs = (
"""
## Layout - Basics
By default each item passed to `view()` are laid out one below the other, with a 10px gap.
```py
view(
    box('Top'),
    box('Middle'),
    box('Bottom'),
)
```
""",
    '### Output',
)


def layout_basic(view: View):
    view(*layout_basic_docs, 
        box('Top'),
        box('Middle'),
        box('Bottom'),
    )


layout_row_docs = (
"""
## Layout - Rows
Use `row()` to lay out multiple items horizontally, left to right.

By default, items take up equal amounts of space, with a `10px` gap between the items.
```py
view(row(
    box('Left'),
    box('Center'),
    box('Right'),
))
```
Setting `row=True` produces the same result as wrapping items with `row()`.
```py
view(
    box('Left'),
    box('Center'),
    box('Right'),
    row=True,
)
```
""",
    '### Output',
)


def layout_row(view: View):
    view(*layout_row_docs, row(
        box('Left'),
        box('Center'),
        box('Right'),
    ))


def layout_row_alt(view: View):
    view(*layout_row_docs, 
        box('Left'),
        box('Center'),
        box('Right'),
        row=True,
    )


layout_col_docs = (
"""
## Layout - Columns
Use `col()` to lay out multiple items vertically, top to bottom.

The example shows one row split into three columns containing three rows each.
```py
view(
    row(
        col(
            box('North-west'),
            box('West'),
            box('South-west'),
        ),
        col(
            box('North'),
            box('Center'),
            box('South'),
        ),
        col(
            box('North-east'),
            box('East'),
            box('South-east'),
        ),
    ),
)
```
""",
    '### Output',
)


def layout_col(view: View):
    view(*layout_col_docs, 
        row(
            col(
                box('North-west'),
                box('West'),
                box('South-west'),
            ),
            col(
                box('North'),
                box('Center'),
                box('South'),
            ),
            col(
                box('North-east'),
                box('East'),
                box('South-east'),
            ),
        ),
    )


layout_size_docs = (
"""
## Layout - Sizing
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
view(
    box(width=200),  # 200px
    box(width='50%'),  # 50% of available width
    box(width='250px'),
    box(width='3in'),
)
```
""",
    '### Output',
)


def layout_size(view: View):
    view(*layout_size_docs, 
        box(width=200),  # 200px
        box(width='50%'),  # 50% of available width
        box(width='250px'),
        box(width='3in'),
    )


layout_gap_docs = (
"""
## Layout - Gap
Set `gap=` to control the spacing between items. The default gap is `10` or `'10px'`.
```py
view(
    box('Top'),
    box('Middle'),
    box('Bottom'),
    gap=25,
)
```
""",
    '### Output',
)


def layout_gap(view: View):
    view(*layout_gap_docs, 
        box('Top'),
        box('Middle'),
        box('Bottom'),
        gap=25,
    )


layout_margin_docs = (
"""
## Layout - Margin
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
    box(text, mode='md', margin='20px', background='#eee'),
    # Same as '20px'
    box(text, mode='md', margin=20, background='#eee'),
    # 0px top and bottom, 100px right and left margin
    box(text, mode='md', margin='0px 100px', background='#eee'),
    # 0px top, 100px right and left, 30px bottom margin
    box(text, mode='md', margin='0px 100px 30px', background='#eee'),
    # 0px top, 100px right, 30px bottom, 200px left margin
    box(text, mode='md', margin='0px 100px 30px 200px', background='#eee'),
]
view(col(*[row(b, border='#000', padding=0) for b in boxes]))
```
""",
    '### Output',
)


def layout_margin(view: View):
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    '''
    boxes = [
        # Uniform 20px margin
        box(text, mode='md', margin='20px', background='#eee'),
        # Same as '20px'
        box(text, mode='md', margin=20, background='#eee'),
        # 0px top and bottom, 100px right and left margin
        box(text, mode='md', margin='0px 100px', background='#eee'),
        # 0px top, 100px right and left, 30px bottom margin
        box(text, mode='md', margin='0px 100px 30px', background='#eee'),
        # 0px top, 100px right, 30px bottom, 200px left margin
        box(text, mode='md', margin='0px 100px 30px 200px', background='#eee'),
    ]
    view(*layout_margin_docs, col(*[row(b, border='#000', padding=0) for b in boxes]))


layout_padding_docs = (
"""
## Layout - Padding
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
        box(text, mode='md', padding='20px', background='#eee'),
        # Same as '20px'
        box(text, mode='md', padding=20, background='#eee'),
        # 0px top and bottom, 100px right and left padding
        box(text, mode='md', padding='0px 100px', background='#eee'),
        # 0px top, 100px right and left, 30px bottom padding
        box(text, mode='md', padding='0px 100px 30px', background='#eee'),
        # 0px top, 100px right, 30px bottom, 200px left padding
        box(text, mode='md', padding='0px 100px 30px 200px', background='#eee'),
    )
)
```
""",
    '### Output',
)


def layout_padding(view: View):
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    '''
    view(*layout_padding_docs, 
        col(
            # Uniform 20px padding
            box(text, mode='md', padding='20px', background='#eee'),
            # Same as '20px'
            box(text, mode='md', padding=20, background='#eee'),
            # 0px top and bottom, 100px right and left padding
            box(text, mode='md', padding='0px 100px', background='#eee'),
            # 0px top, 100px right and left, 30px bottom padding
            box(text, mode='md', padding='0px 100px 30px', background='#eee'),
            # 0px top, 100px right, 30px bottom, 200px left padding
            box(text, mode='md', padding='0px 100px 30px 200px', background='#eee'),
        )
    )


layout_background_docs = (
"""
## Layout - Background Color
Set `background=` to apply a background color.

The text color is automatically changed to a contrasting color if not specified.
A `10px` padding is automatically applied if not specified.
```py
text = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
do eiusmod tempor incididunt ut labore et dolore magna aliqua.
'''
view(
    box(text, mode='md', background='#e63946'),
    box(text, mode='md', background='#f1faee'),
    box(text, mode='md', background='#a8dadc'),
    box(text, mode='md', background='#457b9d'),
    box(text, mode='md', background='#1d3557'),
)
```
""",
    '### Output',
)


def layout_background(view: View):
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    '''
    view(*layout_background_docs, 
        box(text, mode='md', background='#e63946'),
        box(text, mode='md', background='#f1faee'),
        box(text, mode='md', background='#a8dadc'),
        box(text, mode='md', background='#457b9d'),
        box(text, mode='md', background='#1d3557'),
    )


layout_color_docs = (
"""
## Layout - Text Color
Set `color=` to change the text color.
```py
text = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
do eiusmod tempor incididunt ut labore et dolore magna aliqua.
'''
view(
    box(text, mode='md', color='#e63946'),
    box(text, mode='md', color='#457b9d'),
    box(text, mode='md', color='#1d3557'),
)
```
""",
    '### Output',
)


def layout_color(view: View):
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    '''
    view(*layout_color_docs, 
        box(text, mode='md', color='#e63946'),
        box(text, mode='md', color='#457b9d'),
        box(text, mode='md', color='#1d3557'),
    )


layout_border_docs = (
"""
## Layout - Border Color
Set `border=` to add a border.

A `10px` padding is automatically applied if not specified.
```py
text = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
do eiusmod tempor incididunt ut labore et dolore magna aliqua.
'''
view(
    box(text, mode='md', border='#e63946'),
    box(text, mode='md', border='#457b9d'),
    box(text, mode='md', border='#1d3557'),
)
```
""",
    '### Output',
)


def layout_border(view: View):
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    '''
    view(*layout_border_docs, 
        box(text, mode='md', border='#e63946'),
        box(text, mode='md', border='#457b9d'),
        box(text, mode='md', border='#1d3557'),
    )


layout_align_docs = (
"""
## Layout - Align Text
Set `align=` to `left`, `right`, `center` or `justify` to align text.
```py
text = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
'''
view(
    row(
        box(text, mode='md', align='left'),
        box(text, mode='md', align='center'),
        box(text, mode='md', align='justify'),
        box(text, mode='md', align='right'),
        gap=20,
    )
)
```
""",
    '### Output',
)


def layout_align(view: View):
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    '''
    view(*layout_align_docs, 
        row(
            box(text, mode='md', align='left'),
            box(text, mode='md', align='center'),
            box(text, mode='md', align='justify'),
            box(text, mode='md', align='right'),
            gap=20,
        )
    )


layout_tile_docs = (
"""
## Layout - Tile
Set `tile=` to control how items inside a view, row, or column are tiled along the main axis.

- The main axis for a row is horizontal, starting at the left, and ending at the right.
- The main axis for a column is vertical, starting at the top, and ending at the bottom

`tile=` can be set to `start`, `center`, `end`, `between`, `around`, `evenly`, 'stretch', or `normal`.
```py
boxes = [box(text=f'{i + 1}', mode='md', background='#666', width=100) for i in range(3)]
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
""",
    '### Output',
)


def layout_tile(view: View):
    boxes = [box(text=f'{i + 1}', mode='md', background='#666', width=100) for i in range(3)]
    row_style = dict(background='#eee')
    view(*layout_tile_docs, 
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


layout_cross_tile_docs = (
"""
## Layout - Cross-tile
Set `cross_tile=` to control how items inside a view, row, or column are tiled along the cross axis.

- The cross axis for a row is vertical. starting at the top, and ending at the bottom
- The cross axis for a column is horizontal, starting at the left, and ending at the right.

`cross_tile=` can be set to `start`, `center`, `end`, `stretch`, or `normal`.
```py
boxes = [box(text=f'{i + 1}', mode='md', background='#666', width=100) for i in range(3)]
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
""",
    '### Output',
)


def layout_cross_tile(view: View):
    boxes = [box(text=f'{i + 1}', mode='md', background='#666', width=100) for i in range(3)]
    col_style = dict(height=100, background='#eee')
    view(*layout_cross_tile_docs, 
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


layout_wrap_docs = (
"""
## Layout - Wrap
Set `wrap=` to control how items are wrapped inside a view, row, or column.

`wrap=` can be set to `start`, `center`, `end`, `between`, `around`, `evenly`, 'stretch', or `normal`.
```py
boxes = [box(text=f'{i + 1}', mode='md', background='#666', width=150, height=50) for i in range(9)]
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
""",
    '### Output',
)


def layout_wrap(view: View):
    boxes = [box(text=f'{i + 1}', mode='md', background='#666', width=150, height=50) for i in range(9)]
    row_style = dict(height=300, background='#eee')
    view(*layout_wrap_docs, 
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


layout_grow_shrink_docs = (
"""
## Layout - Grow and Shrink
Set `grow=` or `shrink=` to specify what amount of the available space the item should take up
inside a view, row, or column.

Setting `grow=` expands the item. Setting `shrink=` contracts the item. Both are proportions.

By default, items are grown or shrunk based on their initial size. To resize them on a different basis,
set `basis=` to the value you want.

- `basis=0` means "distribute available space assuming that the initial size is zero".
- `basis='20px'` means "distribute available space assuming that the initial size is 20px".
- The default behavior (if `basis=` is not set) is to assume that the initial size is the size of the item's content.
```py
box_style = dict(mode='md', background='#666')
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
""",
    '### Output',
)


def layout_grow_shrink(view: View):
    box_style = dict(mode='md', background='#666')
    row_style = dict(background='#eee')
    view(*layout_grow_shrink_docs, 
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


form_basic_docs = (
"""
## Forms - Basic
To create a form, simply lay out all the inputs you need inside a view, then destructure the return value in order.
```py
username, password, action = view(
    box('Username', value='someone@company.com'),
    box('Password', value='pa55w0rd', password=True),
    box(['Login']),
)
view(f'You entered `{username}`/`{password}` and then clicked on {action}.')
```
""",
    '### Output',
)


def form_basic(view: View):
    username, password, action = view(*form_basic_docs, 
        box('Username', value='someone@company.com'),
        box('Password', value='pa55w0rd', password=True),
        box(['Login']),
    )
    view(*form_basic_docs, f'You entered `{username}`/`{password}` and then clicked on {action}.')


form_horizontal_docs = (
"""
## Forms - Horizontal
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
""",
    '### Output',
)


def form_horizontal(view: View):
    username, password, action = view(*form_horizontal_docs, 
        row(
            box('Username', value='someone@company.com'),
            box('Password', value='pa55w0rd', password=True),
            box(['Login']),
        )
    )
    view(*form_horizontal_docs, f'You entered `{username}`/`{password}` and then clicked on {action}.')


form_combo_docs = (
"""
## Forms - Combined
Use `row()` and `col()` to mix and match how items are laid out. Destructure the return values in the same order.
```py
first, last, addr1, addr2, city, state, zip, action = view(
    row(box('First name'), box('Last name')),
    box('Address line 1'),
    box('Address line 2'),
    row(box('City'), box('State'), box('Zip')),
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
""",
    '### Output',
)


def form_combo(view: View):
    first, last, addr1, addr2, city, state, zip, action = view(*form_combo_docs, 
        row(box('First name'), box('Last name')),
        box('Address line 1'),
        box('Address line 2'),
        row(box('City'), box('State'), box('Zip')),
        box([
            option('yes', 'Sign me up!', selected=True),
            option('no', 'Not now'),
        ])
    )
    view(*form_combo_docs, f'''
    You provided:
    
    Address: {first} {last}, {addr1}, {addr2}, {city} {state} {zip}
    
    Sign up: {action}
    ''')


form_improved_docs = (
"""
## Forms - Improved
Specify additional layout parameters like `width=`, `grow=`, etc. to get more control over
how items are laid out.
```py
first, last, addr1, addr2, city, state, zip, action = view(
    row(box('First name'), box('M.I.', width='10%'), box('Last name')),
    box('Address line 1'),
    box('Address line 2'),
    row(box('City', grow=5), box('State', width='20%'), box('Zip', grow=1)),
    box([
        option('yes', 'Sign me up!', caption='Terms and conditions apply', selected=True),
        option('no', 'Not now', caption="I'll decide later"),
    ])
)
view(f'''
You provided:

Address: {first} {last}, {addr1}, {addr2}, {city} {state} {zip}

Sign up: {action}
''')
```
""",
    '### Output',
)


def form_improved(view: View):
    first, last, addr1, addr2, city, state, zip, action = view(*form_improved_docs, 
        row(box('First name'), box('M.I.', width='10%'), box('Last name')),
        box('Address line 1'),
        box('Address line 2'),
        row(box('City', grow=5), box('State', width='20%'), box('Zip', grow=1)),
        box([
            option('yes', 'Sign me up!', caption='Terms and conditions apply', selected=True),
            option('no', 'Not now', caption="I'll decide later"),
        ])
    )
    view(*form_improved_docs, f'''
    You provided:

    Address: {first} {last}, {addr1}, {addr2}, {city} {state} {zip}

    Sign up: {action}
    ''')


textbox_basic_docs = (
"""
## Textbox - Basic
`box()` without any arguments creates a textbox.
The return value is the text entered into the box.
```py
x = view(box())
view(f'You entered {x}.')
```
""",
    '### Output',
)


def textbox_basic(view: View):
    x = view(*textbox_basic_docs, box())
    view(*textbox_basic_docs, f'You entered {x}.')


textbox_label_docs = (
"""
## Textbox - Label
Any text passed to `box()` is used as a label.
```py
speed = view(box('Speed'))
view(f'Your speed is {speed} km/h.')
```
""",
    '### Output',
)


def textbox_label(view: View):
    speed = view(*textbox_label_docs, box('Speed'))
    view(*textbox_label_docs, f'Your speed is {speed} km/h.')


textbox_value_docs = (
"""
## Textbox - Value
Use `value=` to prefill the box with a value.
```py
speed = view(box('Speed (km/h)', value='60'))
view(f'Your speed is {speed} km/h.')
```
""",
    '### Output',
)


def textbox_value(view: View):
    speed = view(*textbox_value_docs, box('Speed (km/h)', value='60'))
    view(*textbox_value_docs, f'Your speed is {speed} km/h.')


textbox_placeholder_docs = (
"""
## Textbox - Placeholder
Use `placeholder=` to show placeholder text inside the box.
```py
speed = view(box('Speed', placeholder='0 km/h'))
view(f'Your speed is {speed} km/h.')
```
""",
    '### Output',
)


def textbox_placeholder(view: View):
    speed = view(*textbox_placeholder_docs, box('Speed', placeholder='0 km/h'))
    view(*textbox_placeholder_docs, f'Your speed is {speed} km/h.')


textbox_required_docs = (
"""
## Textbox - Required
Set `required=True` to indicate that input is required.
```py
speed = view(box('Speed (km/h)', required=True))
view(f'Your speed is {speed} km/h.')
```
""",
    '### Output',
)


def textbox_required(view: View):
    speed = view(*textbox_required_docs, box('Speed (km/h)', required=True))
    view(*textbox_required_docs, f'Your speed is {speed} km/h.')


textbox_mask_docs = (
"""
## Textbox - Input Mask
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
""",
    '### Output',
)


def textbox_mask(view: View):
    phone = view(*textbox_mask_docs, box('Phone', mask='(999) 999 - 9999'))
    view(*textbox_mask_docs, f'Your phone number is {phone}.')


textbox_icon_docs = (
"""
## Textbox - Icon
Set `icon=` to show an icon at the end of the box.
```py
phrase = view(box('Filter results containing:', icon='Filter'))
view(f'You set a filter on `{phrase}`.')
```
""",
    '### Output',
)


def textbox_icon(view: View):
    phrase = view(*textbox_icon_docs, box('Filter results containing:', icon='Filter'))
    view(*textbox_icon_docs, f'You set a filter on `{phrase}`.')


textbox_prefix_docs = (
"""
## Textbox - Prefix
Set `prefix=` to show a prefix at the start of the box.
```py
website = view(box('Website', prefix='https://', value='example.com'))
view(f'Your website is https://{website}.')
```
""",
    '### Output',
)


def textbox_prefix(view: View):
    website = view(*textbox_prefix_docs, box('Website', prefix='https://', value='example.com'))
    view(*textbox_prefix_docs, f'Your website is https://{website}.')


textbox_suffix_docs = (
"""
## Textbox - Suffix
Set `suffix=` to show a suffix at the end of the box.
```py
website = view(box('Website', suffix='.com', value='example'))
view(f'Your website is {website}.com.')
```
""",
    '### Output',
)


def textbox_suffix(view: View):
    website = view(*textbox_suffix_docs, box('Website', suffix='.com', value='example'))
    view(*textbox_suffix_docs, f'Your website is {website}.com.')


textbox_prefix_suffix_docs = (
"""
## Textbox - Prefix and Suffix
A textbox can show both a prefix and a suffix at the same time.
```py
website = view(box('Website', prefix='https://', suffix='.com', value='example'))
view(f'Your website is https://{website}.com.')
```
""",
    '### Output',
)


def textbox_prefix_suffix(view: View):
    website = view(*textbox_prefix_suffix_docs, box('Website', prefix='https://', suffix='.com', value='example'))
    view(*textbox_prefix_suffix_docs, f'Your website is https://{website}.com.')


textbox_error_docs = (
"""
## Textbox - Error
Set `error=` to show an error message below the box.
```py
speed = view(box('Speed (km/h)', error='Invalid input'))
```
""",
    '### Output',
)


def textbox_error(view: View):
    speed = view(*textbox_error_docs, box('Speed (km/h)', error='Invalid input'))


textbox_password_docs = (
"""
## Textbox - Password
Set `password=True` when accepting passwords and other confidential inputs.
```py
password = view(box('Password field', password=True))
view(f'Your password `{password}` is not strong enough!')
```
""",
    '### Output',
)


def textbox_password(view: View):
    password = view(*textbox_password_docs, box('Password field', password=True))
    view(*textbox_password_docs, f'Your password `{password}` is not strong enough!')


textarea_docs = (
"""
## Textbox - Multiple lines
Set `lines=` to show a multi-line text box (also called a *text area*).
```py
bio = view(box('Bio:', lines=5))
view(f'**Bio:** {bio}')
```
Note that `lines=` only controls the initial height of the textbox, and
multi-line textboxes can be resized by the user.
""",
    '### Output',
)


def textarea(view: View):
    bio = view(*textarea_docs, box('Bio:', lines=5))
    view(*textarea_docs, f'**Bio:** {bio}')


spinbox_basic_docs = (
"""
## Spinbox - Basic
Call `box()` with `mode='number'` to show a box with increment/decrement buttons
(also called a *spinbox*).
```py
speed = view(box('Speed (km/h)', mode='number'))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def spinbox_basic(view: View):
    speed = view(*spinbox_basic_docs, box('Speed (km/h)', mode='number'))
    view(*spinbox_basic_docs, f'Your speed is {speed} km/h')


spinbox_value_docs = (
"""
## Spinbox - Value
Set `value=` to a numeric value to prefill the box with the value.

The mode setting `mode='number'` is implied, and can be elided.
```py
speed = view(box('Speed (km/h)', value=42))
view(f'Your speed is {speed} km/h')
```
In other words, calling `box()` with a numeric `value` has the same effect
as setting `mode='number'`, and is the preferred usage.
""",
    '### Output',
)


def spinbox_value(view: View):
    speed = view(*spinbox_value_docs, box('Speed (km/h)', value=42))
    view(*spinbox_value_docs, f'Your speed is {speed} km/h')


spinbox_min_docs = (
"""
## Spinbox - Min
Set `min=` to specify a minimum value.
```py
speed = view(box('Speed (km/h)', min=10))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def spinbox_min(view: View):
    speed = view(*spinbox_min_docs, box('Speed (km/h)', min=10))
    view(*spinbox_min_docs, f'Your speed is {speed} km/h')


spinbox_max_docs = (
"""
## Spinbox - Max
Set `max=` to specify a maximum value.
```py
speed = view(box('Speed (km/h)', max=100))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def spinbox_max(view: View):
    speed = view(*spinbox_max_docs, box('Speed (km/h)', max=100))
    view(*spinbox_max_docs, f'Your speed is {speed} km/h')


spinbox_step_docs = (
"""
## Spinbox - Step
Set `step=` to specify how much to increment or decrement by.

The default step is `1`.
```py
speed = view(box('Speed (km/h)', step=5))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def spinbox_step(view: View):
    speed = view(*spinbox_step_docs, box('Speed (km/h)', step=5))
    view(*spinbox_step_docs, f'Your speed is {speed} km/h')


spinbox_precision_docs = (
"""
## Spinbox - Precision
Set `precision=` to specify how many decimal places the value should be rounded to.

The default is calculated based on the precision of step:

- if step = 1, precision = 0
- if step = 0.42, precision = 2
- if step = 0.0042, precision = 4
```py
speed = view(box('Speed (m/s)', value=0.6, min=-2, max=2, step=0.2, precision=2))
view(f'Your speed is {speed} m/s')
```
""",
    '### Output',
)


def spinbox_precision(view: View):
    speed = view(*spinbox_precision_docs, box('Speed (m/s)', value=0.6, min=-2, max=2, step=0.2, precision=2))
    view(*spinbox_precision_docs, f'Your speed is {speed} m/s')


spinbox_range_docs = (
"""
## Spinbox - Min, Max, Step, Precision
`min=`, `max=`, `step=` and `precision=` can be combined.
```py
speed = view(box('Speed (km/h)', min=10, max=100, step=5))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def spinbox_range(view: View):
    speed = view(*spinbox_range_docs, box('Speed (km/h)', min=10, max=100, step=5))
    view(*spinbox_range_docs, f'Your speed is {speed} km/h')


spinbox_range_alt_docs = (
"""
## Spinbox - Range
Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.

This is a shorthand notation for setting `min=` and `max=` individually.
```py
speed = view(box('Speed (km/h)', range=(10, 100)))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def spinbox_range_alt(view: View):
    speed = view(*spinbox_range_alt_docs, box('Speed (km/h)', range=(10, 100)))
    view(*spinbox_range_alt_docs, f'Your speed is {speed} km/h')


spinbox_range_alt_step_docs = (
"""
## Spinbox - Range with step
Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.

This is a shorthand notation for setting `min=`, `max=` and `step` individually.
```py
speed = view(box('Speed (km/h)', range=(10, 100, 5)))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def spinbox_range_alt_step(view: View):
    speed = view(*spinbox_range_alt_step_docs, box('Speed (km/h)', range=(10, 100, 5)))
    view(*spinbox_range_alt_step_docs, f'Your speed is {speed} km/h')


spinbox_range_alt_precision_docs = (
"""
## Spinbox - Range with precision
Setting `range=` to a `(min, max, step, precision)` tuple is a shorthand notation for setting
`min=`, `max=`, `step` and `precision` individually.
```py
speed = view(box('Speed (m/s)', value=0.6, range=(-2, 2, 0.2, 2)))
view(f'Your speed is {speed} m/s')
```
""",
    '### Output',
)


def spinbox_range_alt_precision(view: View):
    speed = view(*spinbox_range_alt_precision_docs, box('Speed (m/s)', value=0.6, range=(-2, 2, 0.2, 2)))
    view(*spinbox_range_alt_precision_docs, f'Your speed is {speed} m/s')


spinbox_negative_docs = (
"""
## Spinbox - Zero-crossing range
Ranges can cross zero.
```py
speed = view(box('Speed (m/s)', value=-3, range=(-5, 5)))
view(f'Your speed is {speed} m/s')
```
""",
    '### Output',
)


def spinbox_negative(view: View):
    speed = view(*spinbox_negative_docs, box('Speed (m/s)', value=-3, range=(-5, 5)))
    view(*spinbox_negative_docs, f'Your speed is {speed} m/s')


spinbox_decimal_step_docs = (
"""
## Spinbox - Fractional steps
Steps can be fractional.
```py
speed = view(box('Speed (m/s)', value=0.6, range=(-2, 2, 0.2)))
view(f'Your speed is {speed} m/s')
```
""",
    '### Output',
)


def spinbox_decimal_step(view: View):
    speed = view(*spinbox_decimal_step_docs, box('Speed (m/s)', value=0.6, range=(-2, 2, 0.2)))
    view(*spinbox_decimal_step_docs, f'Your speed is {speed} m/s')


picker_basic_docs = (
"""
## Pickers - Basic
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
""",
    '### Output',
)


def picker_basic(view: View):
    choice = view(*picker_basic_docs, box('Choose a color', options=[
        'green', 'yellow', 'orange', 'red'
    ]))
    view(*picker_basic_docs, f'You chose {choice}.')


picker_buttons_docs = (
"""
## Pickers - Buttons
Buttons are shown for up to 3 options.

Set `mode='button'` to display buttons regardless of the number of options.
```py
choice = view(box('Choose a color', options=[
    'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```
""",
    '### Output',
)


def picker_buttons(view: View):
    choice = view(*picker_buttons_docs, box('Choose a color', options=[
        'yellow', 'orange', 'red'
    ]))
    view(*picker_buttons_docs, f'You chose {choice}.')


picker_radio_docs = (
"""
## Pickers - Radio Buttons
Radio buttons is shown for 4-7 options.

Set `mode='radio'` to display radio buttons regardless of the number of options.
```py
choice = view(box('Choose a color', options=[
    'green', 'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```
""",
    '### Output',
)


def picker_radio(view: View):
    choice = view(*picker_radio_docs, box('Choose a color', options=[
        'green', 'yellow', 'orange', 'red'
    ]))
    view(*picker_radio_docs, f'You chose {choice}.')


picker_dropdown_docs = (
"""
## Pickers - Dropdown
A dropdown menu is shown for more than 7 options.

Set `mode='menu'` to display a dropdown menu regardless of the number of options.
```py
choice = view(box('Choose a color', options=[
    'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```
""",
    '### Output',
)


def picker_dropdown(view: View):
    choice = view(*picker_dropdown_docs, box('Choose a color', options=[
        'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
    ]))
    view(*picker_dropdown_docs, f'You chose {choice}.')


picker_multiple_dropdown_docs = (
"""
## Pickers - Dropdown List
Set `multiple=True` to allow choosing more than one option. The return value is a list of choices made.

By default, this displays checkboxes for up to 7 options, or a dropdown menu for more than 7 options.

Set `mode='menu'` to display a dropdown menu regardless of the number of options.
```py
choices = view(box('Choose some colors', multiple=True, options=[
    'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choices}.')
```
""",
    '### Output',
)


def picker_multiple_dropdown(view: View):
    choices = view(*picker_multiple_dropdown_docs, box('Choose some colors', multiple=True, options=[
        'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
    ]))
    view(*picker_multiple_dropdown_docs, f'You chose {choices}.')


picker_checklist_docs = (
"""
## Pickers - Checklist
A checklist is shown for up to 7 options when `multiple=True`.

Set `mode='check'` to display a checklist regardless of the number of options.
```py
choices = view(box('Choose some colors', mode='check', multiple=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choices}.')
```
""",
    '### Output',
)


def picker_checklist(view: View):
    choices = view(*picker_checklist_docs, box('Choose some colors', mode='check', multiple=True, options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(*picker_checklist_docs, f'You chose {choices}.')


picker_dropdown_required_docs = (
"""
## Pickers - Required
Set `required=True` to indicate that input is required.
```py
choice = view(box('Choose a color', mode='menu', required=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```
""",
    '### Output',
)


def picker_dropdown_required(view: View):
    choice = view(*picker_dropdown_required_docs, box('Choose a color', mode='menu', required=True, options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(*picker_dropdown_required_docs, f'You chose {choice}.')


picker_dropdown_error_docs = (
"""
## Pickers - Error
Set `error=` to show an error message below the box.
```py
choice = view(box('Choose a color', mode='menu', error='Invalid input', options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```
""",
    '### Output',
)


def picker_dropdown_error(view: View):
    choice = view(*picker_dropdown_error_docs, box('Choose a color', mode='menu', error='Invalid input', options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(*picker_dropdown_error_docs, f'You chose {choice}.')


options_basic_docs = (
"""
## Options - Basic
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
""",
    '### Output',
)


def options_basic(view: View):
    choice = view(*options_basic_docs, box('Choose a color', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(*options_basic_docs, f'You chose {choice}.')


options_sequence_docs = (
"""
## Options - From sequence
If `options` is a sequence (tuple, set or list), the elements of the sequence are used as options.
```py
choice = view(box('Choose a color', options=[
    'green', 'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```
""",
    '### Output',
)


def options_sequence(view: View):
    choice = view(*options_sequence_docs, box('Choose a color', options=[
        'green', 'yellow', 'orange', 'red'
    ]))
    view(*options_sequence_docs, f'You chose {choice}.')


options_string_docs = (
"""
## Options - From string
If `options=` is set to a string, each word in the string is used as an option.
```py
choice = view(box('Choose a color', options='green yellow orange red'))
view(f'You chose {choice}.')
```
In other words, `'green yellow orange red'` is a shorthand notation for `['green', 'yellow', 'orange', 'red']`.
""",
    '### Output',
)


def options_string(view: View):
    choice = view(*options_string_docs, box('Choose a color', options='green yellow orange red'))
    view(*options_string_docs, f'You chose {choice}.')


options_tuples_docs = (
"""
## Options - From tuples
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
""",
    '### Output',
)


def options_tuples(view: View):
    choice = view(*options_tuples_docs, box('Choose a color', options=[
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('orange', 'Orange'),
        ('red', 'Red'),
    ]))
    view(*options_tuples_docs, f'You chose {choice}.')


options_dict_docs = (
"""
## Options - From dictionary
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
""",
    '### Output',
)


def options_dict(view: View):
    choice = view(*options_dict_docs, box('Choose a color', options=dict(
        green='Green',
        yellow='Yellow',
        orange='Orange',
        red='Red',
    )))
    view(*options_dict_docs, f'You chose {choice}.')


options_selected_docs = (
"""
## Options - Selected
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
""",
    '### Output',
)


def options_selected(view: View):
    choice = view(*options_selected_docs, box('Choose a color', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(*options_selected_docs, f'You chose {choice}.')


options_value_docs = (
"""
## Options - Value
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
""",
    '### Output',
)


def options_value(view: View):
    choice = view(*options_value_docs, box('Choose a color', value='yellow', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(*options_value_docs, f'You chose {choice}.')


buttons_basic_docs = (
"""
## Buttons - Basic
Set `mode='button'` to show buttons.

`mode=` can be elided when there are 1-3 options.
```py
choice = view(box('Choose a color', mode='button', options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```
""",
    '### Output',
)


def buttons_basic(view: View):
    choice = view(*buttons_basic_docs, box('Choose a color', mode='button', options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(*buttons_basic_docs, f'You chose {choice}.')


buttons_shorthand_docs = (
"""
## Buttons - Shorthand
Most often, it doesn't make sense to show a text prompt above a set of buttons.

In such cases, `box(text=None, mode='button', options=X)` can be shortened to `box(X)`.

In other words, `box()` can accept options instead of text as its first argument.
`mode='button'` is implied.
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
""",
    '### Output',
)


def buttons_shorthand(view: View):
    choice = view(*buttons_shorthand_docs, box(['green', 'yellow', 'orange', 'red']))
    view(*buttons_shorthand_docs, f'You chose {choice}.')


def buttons_shorthand_alt(view: View):
    choice = view(*buttons_shorthand_docs, box([
        option('green', 'Green'),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))

    # Shorter
    choice = view(*buttons_shorthand_docs, box([
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('orange', 'Orange'),
        ('red', 'Red'),
    ]))

    # Shortest
    choice = view(*buttons_shorthand_docs, box(dict(
        green='Green',
        yellow='Yellow',
        orange='Orange',
        red='Red',
    )))


buttons_selected_docs = (
"""
## Buttons - Selected
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
""",
    '### Output',
)


def buttons_selected(view: View):
    choice = view(*buttons_selected_docs, 
        'Updates are available!',
        box([
            option('now', 'Update now', selected=True),
            option('tomorrow', 'Remind me tomorrow'),
            option('never', 'Never update'),
        ])
    )
    view(*buttons_selected_docs, f'You chose to update {choice}.')


buttons_value_docs = (
"""
## Buttons - Value
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
""",
    '### Output',
)


def buttons_value(view: View):
    choice = view(*buttons_value_docs, 
        'Updates are available!',
        box(dict(
            now='Update now',
            tomorrow='Remind me tomorrow',
            never='Never update',
        ), value='now')
    )
    view(*buttons_value_docs, f'You chose to update {choice}.')


buttons_values_docs = (
"""
## Buttons - Values
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
""",
    '### Output',
)


def buttons_values(view: View):
    choice = view(*buttons_values_docs, 
        'Sign me up!',
        box(dict(
            basic='Basic Plan ($9.99/month)',
            pro='Pro Plan ($14.99/month)',
            none='Not interested',
        ), value=['basic', 'pro'])
    )
    view(*buttons_values_docs, f'You chose {choice}.')


buttons_split_docs = (
"""
## Buttons - Split Buttons
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
""",
    '### Output',
)


def buttons_split(view: View):
    choice = view(*buttons_split_docs, 
        'Send fresh donuts every day?',
        box([
            option('yes', 'Yes!', selected=True),
            option('no', 'No', options=[
                option('later', 'Remind me later', icon='ChatBot'),
                option('never', "Don't ask me again", icon='MuteChat'),
            ]),
        ])
    )
    view(*buttons_split_docs, f'You chose {choice}.')


buttons_selected_split_docs = (
"""
## Buttons - Primary Split Buttons
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
""",
    '### Output',
)


def buttons_selected_split(view: View):
    choice = view(*buttons_selected_split_docs, 
        'Send fresh donuts every day?',
        box([
            option('yes', 'Yes!', selected=True, options=[
                option('later', 'Remind me later', icon='ChatBot'),
                option('never', "Don't ask me again", icon='MuteChat'),
            ]),
            option('no', 'No'),
        ])
    )
    view(*buttons_selected_split_docs, f'You chose {choice}.')


buttons_caption_docs = (
"""
## Buttons - Caption
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
""",
    '### Output',
)


def buttons_caption(view: View):
    choice = view(*buttons_caption_docs, 
        'Send fresh donuts every day?',
        box([
            option('yes', 'Sign me up!', caption='Terms and conditions apply', selected=True),
            option('no', 'Not now', caption='I will decide later'),
        ])
    )
    view(*buttons_caption_docs, f'You chose {choice}.')


buttons_layout_docs = (
"""
## Buttons - Layout
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
""",
    '### Output',
)


def buttons_layout(view: View):
    choice = view(*buttons_layout_docs, 
        'Choose a color:',
        box([
            option('auto', 'Automatic', selected=True),
            option('yellow', 'Yellow'),
            option('orange', 'Orange'),
            option('red', 'Red'),
        ], row=False)
    )
    view(*buttons_layout_docs, f'You chose {choice}.')


radio_basic_docs = (
"""
## Radio Buttons - Basic
Set `mode='radio'` to show radio buttons.

`mode=` can be elided when there are 4-7 options.
```py
choice = view(box('Choose a color', mode='radio', options=[
    'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```
""",
    '### Output',
)


def radio_basic(view: View):
    choice = view(*radio_basic_docs, box('Choose a color', mode='radio', options=[
        'blue', 'green', 'yellow', 'orange', 'red', 'black'
    ]))
    view(*radio_basic_docs, f'You chose {choice}.')


radio_value_docs = (
"""
## Radio Buttons - Value
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
""",
    '### Output',
)


def radio_value(view: View):
    choice = view(*radio_value_docs, box('Choose a color', mode='radio', value='yellow', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(*radio_value_docs, f'You chose {choice}.')


radio_selected_docs = (
"""
## Radio Buttons - Selected
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
""",
    '### Output',
)


def radio_selected(view: View):
    choice = view(*radio_selected_docs, box('Choose a color', mode='radio', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(*radio_selected_docs, f'You chose {choice}.')


radio_icon_docs = (
"""
## Radio Buttons - Icons
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
""",
    '### Output',
)


def radio_icon(view: View):
    choice = view(*radio_icon_docs, box('Choose a chart type', mode='radio', options=[
        option('area', 'Area', icon='AreaChart', selected=True),
        option('bar', 'Bar', icon='BarChartHorizontal'),
        option('column', 'Column', icon='BarChartVertical'),
        option('line', 'Line', icon='LineChart'),
        option('scatter', 'Scatter', icon='ScatterChart'),
        option('donut', 'Donut', icon='DonutChart'),
    ]))
    view(*radio_icon_docs, f'You chose {choice}.')


dropdown_basic_docs = (
"""
## Dropdown - Basic
Set `mode='menu'` to show a dropdown menu.

`mode=` can be elided when there are more than 7 options.
```py
choice = view(box('Choose a color', mode='menu', options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```
""",
    '### Output',
)


def dropdown_basic(view: View):
    choice = view(*dropdown_basic_docs, box('Choose a color', mode='menu', options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(*dropdown_basic_docs, f'You chose {choice}.')


dropdown_value_docs = (
"""
## Dropdown - Value
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
""",
    '### Output',
)


def dropdown_value(view: View):
    choice = view(*dropdown_value_docs, box('Choose a color', mode='menu', value='yellow', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(*dropdown_value_docs, f'You chose {choice}.')


dropdown_selected_docs = (
"""
## Dropdown - Selected
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
""",
    '### Output',
)


def dropdown_selected(view: View):
    choice = view(*dropdown_selected_docs, box('Choose a color', mode='menu', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(*dropdown_selected_docs, f'You chose {choice}.')


dropdown_grouped_docs = (
"""
## Dropdown - Grouped
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
""",
    '### Output',
)


def dropdown_grouped(view: View):
    choice = view(*dropdown_grouped_docs, box('Choose a color', options=[
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
    view(*dropdown_grouped_docs, f'You chose {choice}.')


dropdown_editable_docs = (
"""
## Dropdown - Editable
Set `editable=True` to allow arbitrary input in addition to the presented options.

`mode=menu` is implied if `editable=True`.
```py
choice = view(box('Choose a color', editable=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```
""",
    '### Output',
)


def dropdown_editable(view: View):
    choice = view(*dropdown_editable_docs, box('Choose a color', editable=True, options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(*dropdown_editable_docs, f'You chose {choice}.')


multi_dropdown_basic_docs = (
"""
## Dropdown List - Basic
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
""",
    '### Output',
)


def multi_dropdown_basic(view: View):
    choices = view(*multi_dropdown_basic_docs, box(
        'Choose some colors',
        mode='menu',
        multiple=True,
        options=['green', 'yellow', 'orange', 'red']
    ))
    view(*multi_dropdown_basic_docs, f'You chose {choices}.')


multi_dropdown_value_docs = (
"""
## Dropdown List - Value
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
""",
    '### Output',
)


def multi_dropdown_value(view: View):
    choices = view(*multi_dropdown_value_docs, box(
        'Choose some colors',
        mode='menu',
        multiple=True,
        value=['yellow', 'red'],
        options=['green', 'yellow', 'orange', 'red']
    ))
    view(*multi_dropdown_value_docs, f'You chose {choices}.')


multi_dropdown_selected_docs = (
"""
## Dropdown List - Selected
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
""",
    '### Output',
)


def multi_dropdown_selected(view: View):
    choices = view(*multi_dropdown_selected_docs, box(
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
    view(*multi_dropdown_selected_docs, f'You chose {choices}.')


checklist_basic_docs = (
"""
## Checklist - Basic
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
""",
    '### Output',
)


def checklist_basic(view: View):
    choices = view(*checklist_basic_docs, box(
        'Choose some colors',
        mode='check',
        multiple=True,
        options=['green', 'yellow', 'orange', 'red']
    ))
    view(*checklist_basic_docs, f'You chose {choices}.')


checklist_value_docs = (
"""
## Checklist - Value
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
""",
    '### Output',
)


def checklist_value(view: View):
    choices = view(*checklist_value_docs, box(
        'Choose some colors',
        mode='check',
        multiple=True,
        value=['yellow', 'red'],
        options=['green', 'yellow', 'orange', 'red']
    ))
    view(*checklist_value_docs, f'You chose {choices}.')


checklist_selected_docs = (
"""
## Checklist - Selected
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
""",
    '### Output',
)


def checklist_selected(view: View):
    choices = view(*checklist_selected_docs, box(
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
    view(*checklist_selected_docs, f'You chose {choices}.')


slider_basic_docs = (
"""
## Slider - Basic
Set `mode='range'` to show a slider.

The default range is between `0` and `10`.
```py
speed = view(box('Speed (km/h)', mode='range'))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def slider_basic(view: View):
    speed = view(*slider_basic_docs, box('Speed (km/h)', mode='range'))
    view(*slider_basic_docs, f'Your speed is {speed} km/h')


slider_value_docs = (
"""
## Slider - Value
Set `value=` to default the slider value.
```py
speed = view(box('Speed (km/h)', mode='range', value=5))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def slider_value(view: View):
    speed = view(*slider_value_docs, box('Speed (km/h)', mode='range', value=5))
    view(*slider_value_docs, f'Your speed is {speed} km/h')


slider_min_docs = (
"""
## Slider - Min
Set `min=` to specify a minimum value.
```py
speed = view(box('Speed (km/h)', mode='range', min=3))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def slider_min(view: View):
    speed = view(*slider_min_docs, box('Speed (km/h)', mode='range', min=3))
    view(*slider_min_docs, f'Your speed is {speed} km/h')


slider_max_docs = (
"""
## Slider - Max
Set `max=` to specify a maximum value.
```py
speed = view(box('Speed (km/h)', mode='range', max=100))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def slider_max(view: View):
    speed = view(*slider_max_docs, box('Speed (km/h)', mode='range', max=100))
    view(*slider_max_docs, f'Your speed is {speed} km/h')


slider_step_docs = (
"""
## Slider - Step
Set `step=` to specify how much to increment or decrement by.

The default step is `1`.
```py
speed = view(box('Speed (km/h)', mode='range', step=2))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def slider_step(view: View):
    speed = view(*slider_step_docs, box('Speed (km/h)', mode='range', step=2))
    view(*slider_step_docs, f'Your speed is {speed} km/h')


slider_precision_docs = (
"""
## Slider - Precision
Set `precision=` to specify how many decimal places the value should be rounded to.

The default is calculated based on the precision of step:

- if step = 1, precision = 0
- if step = 0.42, precision = 2
- if step = 0.0042, precision = 4
```py
speed = view(box('Speed (m/s)', mode='range', value=0.6, min=-2, max=2, step=0.2, precision=2))
view(f'Your speed is {speed} m/s')
```
""",
    '### Output',
)


def slider_precision(view: View):
    speed = view(*slider_precision_docs, box('Speed (m/s)', mode='range', value=0.6, min=-2, max=2, step=0.2, precision=2))
    view(*slider_precision_docs, f'Your speed is {speed} m/s')


slider_range_docs = (
"""
## Slider - Min, Max, Step, Precision
`min=`, `max=`, `step=` and `precision=` can be combined.
```py
speed = view(box('Speed (km/h)', mode='range', min=10, max=100, step=5))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def slider_range(view: View):
    speed = view(*slider_range_docs, box('Speed (km/h)', mode='range', min=10, max=100, step=5))
    view(*slider_range_docs, f'Your speed is {speed} km/h')


slider_range_alt_docs = (
"""
## Slider - Range
Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.

This is a shorthand notation for setting `min=` and `max=` individually.
```py
speed = view(box('Speed (km/h)', mode='range', range=(10, 100)))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def slider_range_alt(view: View):
    speed = view(*slider_range_alt_docs, box('Speed (km/h)', mode='range', range=(10, 100)))
    view(*slider_range_alt_docs, f'Your speed is {speed} km/h')


slider_range_alt_step_docs = (
"""
## Slider - Range with step
Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.

This is a shorthand notation for setting `min=`, `max=` and `step` individually.
```py
speed = view(box('Speed (km/h)', mode='range', range=(10, 100, 5)))
view(f'Your speed is {speed} km/h')
```
""",
    '### Output',
)


def slider_range_alt_step(view: View):
    speed = view(*slider_range_alt_step_docs, box('Speed (km/h)', mode='range', range=(10, 100, 5)))
    view(*slider_range_alt_step_docs, f'Your speed is {speed} km/h')


slider_range_alt_precision_docs = (
"""
## Slider - Range with precision
Setting `range=` to a `(min, max, step, precision)` tuple is a shorthand notation for setting
`min=`, `max=`, `step` and `precision` individually.
```py
speed = view(box('Speed (m/s)', mode='range', value=0.6, range=(-2, 2, 0.2, 2)))
view(f'Your speed is {speed} m/s')
```
""",
    '### Output',
)


def slider_range_alt_precision(view: View):
    speed = view(*slider_range_alt_precision_docs, box('Speed (m/s)', mode='range', value=0.6, range=(-2, 2, 0.2, 2)))
    view(*slider_range_alt_precision_docs, f'Your speed is {speed} m/s')


slider_negative_docs = (
"""
## Slider - Zero-crossing range
Ranges can cross zero.
```py
speed = view(box('Speed (m/s)', mode='range', value=-3, range=(-5, 5)))
view(f'Your speed is {speed} m/s')
```
""",
    '### Output',
)


def slider_negative(view: View):
    speed = view(*slider_negative_docs, box('Speed (m/s)', mode='range', value=-3, range=(-5, 5)))
    view(*slider_negative_docs, f'Your speed is {speed} m/s')


slider_decimal_step_docs = (
"""
## Slider - Fractional steps
Steps can be fractional.
```py
speed = view(box('Speed (m/s)', mode='range', value=0.6, range=(-2, 2, 0.2)))
view(f'Your speed is {speed} m/s')
```
""",
    '### Output',
)


def slider_decimal_step(view: View):
    speed = view(*slider_decimal_step_docs, box('Speed (m/s)', mode='range', value=0.6, range=(-2, 2, 0.2)))
    view(*slider_decimal_step_docs, f'Your speed is {speed} m/s')


range_slider_basic_docs = (
"""
## Range Slider - Basic
Set `value=` to a `(start, end)` tuple to show a range slider.

The mode setting `mode='range'` is implied, and can be elided.
```py
start, end = view(box('Speed range (km/h)', value=(3, 7)))
view(f'Your speed ranges between {start} and {end} km/h')
```
""",
    '### Output',
)


def range_slider_basic(view: View):
    start, end = view(*range_slider_basic_docs, box('Speed range (km/h)', value=(3, 7)))
    view(*range_slider_basic_docs, f'Your speed ranges between {start} and {end} km/h')


range_slider_min_docs = (
"""
## Range Slider - Min
Set `min=` to specify a minimum value.
```py
start, end = view(box('Speed range (km/h)', value=(3, 7), min=3))
view(f'Your speed ranges between {start} and {end} km/h')
```
""",
    '### Output',
)


def range_slider_min(view: View):
    start, end = view(*range_slider_min_docs, box('Speed range (km/h)', value=(3, 7), min=3))
    view(*range_slider_min_docs, f'Your speed ranges between {start} and {end} km/h')


range_slider_max_docs = (
"""
## Range Slider - Max
Set `max=` to specify a maximum value.
```py
start, end = view(box('Speed range (km/h)', value=(30, 70), max=100))
view(f'Your speed ranges between {start} and {end} km/h')
```
""",
    '### Output',
)


def range_slider_max(view: View):
    start, end = view(*range_slider_max_docs, box('Speed range (km/h)', value=(30, 70), max=100))
    view(*range_slider_max_docs, f'Your speed ranges between {start} and {end} km/h')


range_slider_step_docs = (
"""
## Range Slider - Step
Set `step=` to specify how much to increment or decrement by.

The default step is `1`.
```py
start, end = view(box('Speed range (km/h)', value=(2, 6), step=2))
view(f'Your speed ranges between {start} and {end} km/h')
```
""",
    '### Output',
)


def range_slider_step(view: View):
    start, end = view(*range_slider_step_docs, box('Speed range (km/h)', value=(2, 6), step=2))
    view(*range_slider_step_docs, f'Your speed ranges between {start} and {end} km/h')


range_slider_precision_docs = (
"""
## Range Slider - Precision
Set `precision=` to specify how many decimal places the value should be rounded to.

The default is calculated based on the precision of step:
- if step = 1, precision = 0
- if step = 0.42, precision = 2
- if step = 0.0042, precision = 4
```py
start, end = view(box('Speed range (m/s)', value=(-0.4, 0.4), min=-2, max=2, step=0.2, precision=2))
view(f'Your speed ranges between {start} and {end} m/s')
```
""",
    '### Output',
)


def range_slider_precision(view: View):
    start, end = view(*range_slider_precision_docs, box('Speed range (m/s)', value=(-0.4, 0.4), min=-2, max=2, step=0.2, precision=2))
    view(*range_slider_precision_docs, f'Your speed ranges between {start} and {end} m/s')


range_slider_range_docs = (
"""
## Range Slider - Min, Max, Step, Precision
`min=`, `max=`, `step=` and `precision=` can be combined.
```py
start, end = view(box('Speed range (km/h)', value=(30, 70), min=10, max=100, step=5))
view(f'Your speed ranges between {start} and {end} km/h')
```
""",
    '### Output',
)


def range_slider_range(view: View):
    start, end = view(*range_slider_range_docs, box('Speed range (km/h)', value=(30, 70), min=10, max=100, step=5))
    view(*range_slider_range_docs, f'Your speed ranges between {start} and {end} km/h')


range_slider_range_alt_docs = (
"""
## Range Slider - Range
Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.

This is a shorthand notation for setting `min=` and `max=` individually.
```py
start, end = view(box('Speed range (km/h)', value=(30, 70), range=(10, 100)))
view(f'Your speed ranges between {start} and {end} km/h')
```
""",
    '### Output',
)


def range_slider_range_alt(view: View):
    start, end = view(*range_slider_range_alt_docs, box('Speed range (km/h)', value=(30, 70), range=(10, 100)))
    view(*range_slider_range_alt_docs, f'Your speed ranges between {start} and {end} km/h')


range_slider_range_alt_step_docs = (
"""
## Range Slider - Range with step
Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.

This is a shorthand notation for setting `min=`, `max=` and `step` individually.
```py
start, end = view(box('Speed range (km/h)', value=(30, 70), range=(10, 100, 5)))
view(f'Your speed ranges between {start} and {end} km/h')
```
""",
    '### Output',
)


def range_slider_range_alt_step(view: View):
    start, end = view(*range_slider_range_alt_step_docs, box('Speed range (km/h)', value=(30, 70), range=(10, 100, 5)))
    view(*range_slider_range_alt_step_docs, f'Your speed ranges between {start} and {end} km/h')


range_slider_range_alt_precision_docs = (
"""
## Range Slider - Range with precision
Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.
Setting `range=` to a `(min, max, step, precision)` tuple is a shorthand notation for setting
`min=`, `max=`, `step` and `precision` individually.
```py
start, end = view(box('Speed range (m/s)', value=(-0.4, 0.4), range=(-2, 2, 0.2, 2)))
view(f'Your speed ranges between {start} and {end} m/s')
```
""",
    '### Output',
)


def range_slider_range_alt_precision(view: View):
    start, end = view(*range_slider_range_alt_precision_docs, box('Speed range (m/s)', value=(-0.4, 0.4), range=(-2, 2, 0.2, 2)))
    view(*range_slider_range_alt_precision_docs, f'Your speed ranges between {start} and {end} m/s')


range_slider_negative_docs = (
"""
## Range Slider - Zero-crossing range
Ranges can cross zero.
```py
start, end = view(box('Speed range (m/s)', value=(-3, 3), range=(-5, 5)))
view(f'Your speed ranges between {start} and {end} m/s')
```
""",
    '### Output',
)


def range_slider_negative(view: View):
    start, end = view(*range_slider_negative_docs, box('Speed range (m/s)', value=(-3, 3), range=(-5, 5)))
    view(*range_slider_negative_docs, f'Your speed ranges between {start} and {end} m/s')


range_slider_decimal_step_docs = (
"""
## Range Slider - Fractional steps
Steps can be fractional.
```py
start, end = view(box('Speed range (m/s)', value=(-0.4, 0.4), range=(-2, 2, 0.2)))
view(f'Your speed ranges between {start} and {end} m/s')
```
""",
    '### Output',
)


def range_slider_decimal_step(view: View):
    start, end = view(*range_slider_decimal_step_docs, box('Speed range (m/s)', value=(-0.4, 0.4), range=(-2, 2, 0.2)))
    view(*range_slider_decimal_step_docs, f'Your speed ranges between {start} and {end} m/s')


time_basic_docs = (
"""
## Time Picker - Basic
Set `mode='time'` to show a time picker.
```py
time = view(box('Set alarm for:', mode='time', value='3:04PM'))
view(f'Alarm set for {time}.')
```
""",
    '### Output',
)


def time_basic(view: View):
    time = view(*time_basic_docs, box('Set alarm for:', mode='time', value='3:04PM'))
    view(*time_basic_docs, f'Alarm set for {time}.')


time_seconds_docs = (
"""
## Time Picker - With seconds
Include seconds in the `value` to show a seconds component.
```py
time = view(box('Set alarm for:', mode='time', value='3:04:05PM'))
view(f'Alarm set for {time}.')
```
""",
    '### Output',
)


def time_seconds(view: View):
    time = view(*time_seconds_docs, box('Set alarm for:', mode='time', value='3:04:05PM'))
    view(*time_seconds_docs, f'Alarm set for {time}.')


time_hour_docs = (
"""
## Time Picker - Hour only
Exclude minutes and seconds from the `value` to show only the hour component.
```py
time = view(box('Set alarm for:', mode='time', value='3PM'))
view(f'Alarm set for {time}.')
```
""",
    '### Output',
)


def time_hour(view: View):
    time = view(*time_hour_docs, box('Set alarm for:', mode='time', value='3PM'))
    view(*time_hour_docs, f'Alarm set for {time}.')


time_24_docs = (
"""
## Time Picker - 24-hour clock
Exclude `AM` or `PM` from the `value` to accept input in military time.
```py
time = view(box('Set alarm for:', mode='time', value='15:04'))
view(f'Alarm set for {time}.')
```
""",
    '### Output',
)


def time_24(view: View):
    time = view(*time_24_docs, box('Set alarm for:', mode='time', value='15:04'))
    view(*time_24_docs, f'Alarm set for {time}.')


time_24_seconds_docs = (
"""
## Time Picker - 24-hour clock, with seconds
Include seconds in the `value` to show a seconds component.
```py
time = view(box('Set alarm for:', mode='time', value='15:04:05'))
view(f'Alarm set for {time}.')
```
""",
    '### Output',
)


def time_24_seconds(view: View):
    time = view(*time_24_seconds_docs, box('Set alarm for:', mode='time', value='15:04:05'))
    view(*time_24_seconds_docs, f'Alarm set for {time}.')


time_24_hour_docs = (
"""
## Time Picker - 24-hour clock, hour only
Exclude minutes and seconds from the `value` to show only the hour component.
```py
time = view(box('Set alarm for:', mode='time', value='15'))
view(f'Alarm set for {time}.')
```
""",
    '### Output',
)


def time_24_hour(view: View):
    time = view(*time_24_hour_docs, box('Set alarm for:', mode='time', value='15'))
    view(*time_24_hour_docs, f'Alarm set for {time}.')


date_basic_docs = (
"""
## Date Picker - Basic
Set `mode='date'` to show a date-picker.
```py
date = view(box('Pick a date', mode='date'))
view(f'You picked {date}.')
```
""",
    '### Output',
)


def date_basic(view: View):
    date = view(*date_basic_docs, box('Pick a date', mode='date'))
    view(*date_basic_docs, f'You picked {date}.')


date_placeholder_docs = (
"""
## Date Picker - Placeholder
Set `placeholder=` to show placeholder text.
```py
date = view(box('Deliver on', mode='date', placeholder='Delivery date'))
view(f'You picked {date}.')
```
""",
    '### Output',
)


def date_placeholder(view: View):
    date = view(*date_placeholder_docs, box('Deliver on', mode='date', placeholder='Delivery date'))
    view(*date_placeholder_docs, f'You picked {date}.')


date_required_docs = (
"""
## Date Picker - Required
Set `required=True` to indicate that input is required.
```py
date = view(box('Pick a date', mode='date', required=True))
view(f'You picked {date}.')
```
""",
    '### Output',
)


def date_required(view: View):
    date = view(*date_required_docs, box('Pick a date', mode='date', required=True))
    view(*date_required_docs, f'You picked {date}.')


date_value_docs = (
"""
## Date Picker - Value
Set `value=` to pre-select a date.

Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.
```py
date = view(box('Pick a date', mode='date', value='2021-10-10'))
view(f'You picked {date}.')
```
""",
    '### Output',
)


def date_value(view: View):
    date = view(*date_value_docs, box('Pick a date', mode='date', value='2021-10-10'))
    view(*date_value_docs, f'You picked {date}.')


date_min_docs = (
"""
## Date Picker - Min
Set `min=` to specify a minimum date.
```py
date = view(box('Pick a date', mode='date', value='2021-10-10', min='2019-01-01'))
view(f'You picked {date}.')
```
""",
    '### Output',
)


def date_min(view: View):
    date = view(*date_min_docs, box('Pick a date', mode='date', value='2021-10-10', min='2019-01-01'))
    view(*date_min_docs, f'You picked {date}.')


date_max_docs = (
"""
## Date Picker - Max
Set `max=` to specify a maximum date.
```py
date = view(box('Pick a date', mode='date', value='2021-10-10', max='2022-12-31'))
view(f'You picked {date}.')
```
""",
    '### Output',
)


def date_max(view: View):
    date = view(*date_max_docs, box('Pick a date', mode='date', value='2021-10-10', max='2022-12-31'))
    view(*date_max_docs, f'You picked {date}.')


date_min_max_docs = (
"""
## Date Picker - Min and Max
Set both `min=` and `max=` to restrict selection between two dates.
```py
date = view(box('Pick a date', mode='date', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
view(f'You picked {date}.')
```
""",
    '### Output',
)


def date_min_max(view: View):
    date = view(*date_min_max_docs, box('Pick a date', mode='date', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
    view(*date_min_max_docs, f'You picked {date}.')


date_range_docs = (
"""
## Date Picker - Range
Set `range=` to a `(min, max)` tuple to restrict selection between two dates.

This is a shorthand notation for setting `min=` and `max=` individually.
```py
date = view(box('Pick a date', mode='date', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
view(f'You picked {date}.')
```
""",
    '### Output',
)


def date_range(view: View):
    date = view(*date_range_docs, box('Pick a date', mode='date', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    view(*date_range_docs, f'You picked {date}.')


day_basic_docs = (
"""
## Calendar - Basic
Set `mode='day'` to show a calendar.
```py
date = view(box('Pick a date', mode='day'))
view(f'You picked {date}.')
```
""",
    '### Output',
)


def day_basic(view: View):
    date = view(*day_basic_docs, box('Pick a date', mode='day'))
    view(*day_basic_docs, f'You picked {date}.')


day_value_docs = (
"""
## Calendar - Value
Set `value=` to pre-select a date.

Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.
```py
date = view(box('Pick a date', mode='day', value='2021-10-10'))
view(f'You picked {date}.')
```
""",
    '### Output',
)


def day_value(view: View):
    date = view(*day_value_docs, box('Pick a date', mode='day', value='2021-10-10'))
    view(*day_value_docs, f'You picked {date}.')


day_min_docs = (
"""
## Calendar - Min
Set `min=` to specify a minimum date.
```py
date = view(box('Pick a date', mode='day', value='2021-10-10', min='2019-01-01'))
view(f'You picked {date}.')
```
""",
    '### Output',
)


def day_min(view: View):
    date = view(*day_min_docs, box('Pick a date', mode='day', value='2021-10-10', min='2019-01-01'))
    view(*day_min_docs, f'You picked {date}.')


day_max_docs = (
"""
## Calendar - Max
Set `max=` to specify a maximum date.
```py
date = view(box('Pick a date', mode='day', value='2021-10-10', max='2022-12-31'))
view(f'You picked {date}.')
```
""",
    '### Output',
)


def day_max(view: View):
    date = view(*day_max_docs, box('Pick a date', mode='day', value='2021-10-10', max='2022-12-31'))
    view(*day_max_docs, f'You picked {date}.')


day_min_max_docs = (
"""
## Calendar - Min and Max
Set both `min=` and `max=` to restrict selection between two dates.
```py
date = view(box('Pick a date', mode='day', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
view(f'You picked {date}.')
```
""",
    '### Output',
)


def day_min_max(view: View):
    date = view(*day_min_max_docs, box('Pick a date', mode='day', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
    view(*day_min_max_docs, f'You picked {date}.')


day_range_docs = (
"""
## Calendar - Range
Set `range=` to a `(min, max)` tuple to restrict selection between two dates.

This is a shorthand notation for setting `min=` and `max=` individually.
```py
date = view(box('Pick a date', mode='day', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
view(f'You picked {date}.')
```
""",
    '### Output',
)


def day_range(view: View):
    date = view(*day_range_docs, box('Pick a date', mode='day', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    view(*day_range_docs, f'You picked {date}.')


week_basic_docs = (
"""
## Week Picker - Basic
Set `mode='week'` to show a week picker.
```py
week = view(box('Pick a week', mode='week'))
view(f'You picked {week}.')
```
""",
    '### Output',
)


def week_basic(view: View):
    week = view(*week_basic_docs, box('Pick a week', mode='week'))
    view(*week_basic_docs, f'You picked {week}.')


week_value_docs = (
"""
## Week Picker - Value
Set `value=` to pre-select a week.

Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.
```py
week = view(box('Pick a week', mode='week', value='2021-10-10'))
view(f'You picked {week}.')
```
""",
    '### Output',
)


def week_value(view: View):
    week = view(*week_value_docs, box('Pick a week', mode='week', value='2021-10-10'))
    view(*week_value_docs, f'You picked {week}.')


week_min_docs = (
"""
## Week Picker - Min
Set `min=` to specify a minimum date.
```py
week = view(box('Pick a week', mode='week', value='2021-10-10', min='2019-01-01'))
view(f'You picked {week}.')
```
""",
    '### Output',
)


def week_min(view: View):
    week = view(*week_min_docs, box('Pick a week', mode='week', value='2021-10-10', min='2019-01-01'))
    view(*week_min_docs, f'You picked {week}.')


week_max_docs = (
"""
## Week Picker - Max
Set `max=` to specify a maximum date.
```py
week = view(box('Pick a week', mode='week', value='2021-10-10', max='2022-12-31'))
view(f'You picked {week}.')
```
""",
    '### Output',
)


def week_max(view: View):
    week = view(*week_max_docs, box('Pick a week', mode='week', value='2021-10-10', max='2022-12-31'))
    view(*week_max_docs, f'You picked {week}.')


week_min_max_docs = (
"""
## Week Picker - Min and Max
Set both `min=` and `max=` to restrict selection between two dates.
```py
week = view(box('Pick a week', mode='week', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
view(f'You picked {week}.')
```
""",
    '### Output',
)


def week_min_max(view: View):
    week = view(*week_min_max_docs, box('Pick a week', mode='week', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
    view(*week_min_max_docs, f'You picked {week}.')


week_range_docs = (
"""
## Week Picker - Range
Set `range=` to a `(min, max)` tuple to restrict selection between two dates.

This is a shorthand notation for setting `min=` and `max=` individually.
```py
week = view(box('Pick a week', mode='week', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
view(f'You picked {week}.')
```
""",
    '### Output',
)


def week_range(view: View):
    week = view(*week_range_docs, box('Pick a week', mode='week', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    view(*week_range_docs, f'You picked {week}.')


month_basic_docs = (
"""
## Month Picker - Basic
Set `mode='month'` to show a month picker.
```py
month = view(box('Pick a month', mode='month'))
view(f'You picked {month}.')
```
""",
    '### Output',
)


def month_basic(view: View):
    month = view(*month_basic_docs, box('Pick a month', mode='month'))
    view(*month_basic_docs, f'You picked {month}.')


month_value_docs = (
"""
## Month Picker - Value
Set `value=` to pre-select a month.

Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.
```py
month = view(box('Pick a month', mode='month', value='2021-10-10'))
view(f'You picked {month}.')
```
""",
    '### Output',
)


def month_value(view: View):
    month = view(*month_value_docs, box('Pick a month', mode='month', value='2021-10-10'))
    view(*month_value_docs, f'You picked {month}.')


month_min_docs = (
"""
## Month Picker - Min
Set `min=` to specify a minimum date.
```py
month = view(box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01'))
view(f'You picked {month}.')
```
""",
    '### Output',
)


def month_min(view: View):
    month = view(*month_min_docs, box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01'))
    view(*month_min_docs, f'You picked {month}.')


month_max_docs = (
"""
## Month Picker - Max
Set `max=` to specify a maximum date.
```py
month = view(box('Pick a month', mode='month', value='2021-10-10', max='2022-12-31'))
view(f'You picked {month}.')
```
""",
    '### Output',
)


def month_max(view: View):
    month = view(*month_max_docs, box('Pick a month', mode='month', value='2021-10-10', max='2022-12-31'))
    view(*month_max_docs, f'You picked {month}.')


month_min_max_docs = (
"""
## Month Picker - Min and Max
Set both `min=` and `max=` to restrict selection between two dates.
```py
month = view(box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
view(f'You picked {month}.')
```
""",
    '### Output',
)


def month_min_max(view: View):
    month = view(*month_min_max_docs, box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
    view(*month_min_max_docs, f'You picked {month}.')


month_range_docs = (
"""
## Month Picker - Range
Set `range=` to a `(min, max)` tuple to restrict selection between two dates.

This is a shorthand notation for setting `min=` and `max=` individually.
```py
month = view(box('Pick a month', mode='month', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
view(f'You picked {month}.')
```
""",
    '### Output',
)


def month_range(view: View):
    month = view(*month_range_docs, box('Pick a month', mode='month', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    view(*month_range_docs, f'You picked {month}.')


tag_picker_basic_docs = (
"""
## Tag Picker - Basic
Set `mode='tag'` to display a tag picker. `multiple=True` is implied.
```py
tags = view(box(
    'Choose some tags',
    mode='tag',
    options=['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']
))
view(f'You chose {tags}.')
```
""",
    '### Output',
)


def tag_picker_basic(view: View):
    tags = view(*tag_picker_basic_docs, box(
        'Choose some tags',
        mode='tag',
        options=['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']
    ))
    view(*tag_picker_basic_docs, f'You chose {tags}.')


tag_picker_value_docs = (
"""
## Tag Picker - Value
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
""",
    '### Output',
)


def tag_picker_value(view: View):
    tags = view(*tag_picker_value_docs, box(
        'Choose some tags',
        mode='tag',
        value=['yellow', 'red'],
        options=['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']
    ))
    view(*tag_picker_value_docs, f'You chose {tags}.')


tag_picker_selected_docs = (
"""
## Tag Picker - Selected
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
""",
    '### Output',
)


def tag_picker_selected(view: View):
    tags = view(*tag_picker_selected_docs, box('Choose some tags', mode='tag', options=[
        option('violet', 'Violet'),
        option('indigo', 'Indigo'),
        option('blue', 'Blue'),
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red', selected=True),
    ]))
    view(*tag_picker_selected_docs, f'You chose {tags}.')


color_basic_docs = (
"""
## Color Picker - Basic
Set `mode='color'` to show a color picker.

The return value is a `(r, g, b, a)` tuple,
where `r`, `g`, `b` are integers between 0-255,
and `a` is an integer between 0-100%.
```py
color = view(box('Choose a color', mode='color'))
r, g, b, a = color
view(f'You chose the color `rgba({r}, {g}, {b}, {a}%)`.')
```
""",
    '### Output',
)


def color_basic(view: View):
    color = view(*color_basic_docs, box('Choose a color', mode='color'))
    r, g, b, a = color
    view(*color_basic_docs, f'You chose the color `rgba({r}, {g}, {b}, {a}%)`.')


color_value_docs = (
"""
## Color Picker - Value
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
""",
    '### Output',
)


def color_value(view: View):
    color = view(*color_value_docs, box('Choose a color', mode='color', value='#a241e8'))
    view(*color_value_docs, f'You chose {color}.')


palette_basic_docs = (
"""
## Color Palette - Basic
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
""",
    '### Output',
)


def palette_basic(view: View):
    color = view(*palette_basic_docs, box('Choose a color', mode='color', options=[
        option('#ff0000', 'Red'),
        option('#00ff00', 'Green'),
        option('#0000ff', 'Blue'),
        option('#ffff00', 'Yellow'),
        option('#00ffff', 'Cyan'),
        option('#ff00ff', 'Magenta'),
    ]))
    view(*palette_basic_docs, f'You chose {color}.')


palette_value_docs = (
"""
## Color Palette - Value
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
""",
    '### Output',
)


def palette_value(view: View):
    color = view(*palette_value_docs, box('Choose a color', mode='color', value='#0000ff', options=[
        option('#ff0000', 'Red'),
        option('#00ff00', 'Green'),
        option('#0000ff', 'Blue'),
        option('#ffff00', 'Yellow'),
        option('#00ffff', 'Cyan'),
        option('#ff00ff', 'Magenta'),
    ]))
    view(*palette_value_docs, f'You chose {color}.')


palette_selected_docs = (
"""
## Color Palette - Selected
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
""",
    '### Output',
)


def palette_selected(view: View):
    color = view(*palette_selected_docs, box('Choose a color', mode='color', options=[
        option('#ff0000', 'Red'),
        option('#00ff00', 'Green'),
        option('#0000ff', 'Blue', selected=True),
        option('#ffff00', 'Yellow'),
        option('#00ffff', 'Cyan'),
        option('#ff00ff', 'Magenta'),
    ]))
    view(*palette_selected_docs, f'You chose {color}.')


rating_basic_docs = (
"""
## Rating - Basic
Set `mode='rating'` to accept a star-rating.

By default, five stars are displayed.
```py
stars = view(box('Rate your experience', mode='rating'))
view(f'Your rating was {stars} stars.')
```
""",
    '### Output',
)


def rating_basic(view: View):
    stars = view(*rating_basic_docs, box('Rate your experience', mode='rating'))
    view(*rating_basic_docs, f'Your rating was {stars} stars.')


rating_value_docs = (
"""
## Rating - Value
Set `value=` to specify a default value.
```py
stars = view(box('Rate your experience', mode='rating', value=3))
view(f'Your rating was {stars} stars.')
```
""",
    '### Output',
)


def rating_value(view: View):
    stars = view(*rating_value_docs, box('Rate your experience', mode='rating', value=3))
    view(*rating_value_docs, f'Your rating was {stars} stars.')


rating_min_docs = (
"""
## Rating - Min
Set `min=0` to allow zero stars.
```py
stars = view(box('Rate your experience', mode='rating', min=0))
view(f'Your rating was {stars} stars.')
```
""",
    '### Output',
)


def rating_min(view: View):
    stars = view(*rating_min_docs, box('Rate your experience', mode='rating', min=0))
    view(*rating_min_docs, f'Your rating was {stars} stars.')


rating_max_docs = (
"""
## Rating - Max
Set `max=` to increase the number of stars displayed.
```py
stars = view(box('Rate your experience', mode='rating', value=3, max=10))
view(f'Your rating was {stars} stars.')
```
""",
    '### Output',
)


def rating_max(view: View):
    stars = view(*rating_max_docs, box('Rate your experience', mode='rating', value=3, max=10))
    view(*rating_max_docs, f'Your rating was {stars} stars.')


rating_min_max_docs = (
"""
## Rating - Min and max
`min=` and `max=` can be combined.
```py
stars = view(box('Rate your experience', mode='rating', value=3, min=0, max=10))
view(f'Your rating was {stars} stars.')
```
""",
    '### Output',
)


def rating_min_max(view: View):
    stars = view(*rating_min_max_docs, box('Rate your experience', mode='rating', value=3, min=0, max=10))
    view(*rating_min_max_docs, f'Your rating was {stars} stars.')


rating_range_docs = (
"""
## Rating - Range
Set `range=` to a `(min, max)` tuple to control min/max stars.

This is a shorthand notation for setting `min=` and `max=` individually.
```py
stars = view(box('Rate your experience', mode='rating', value=3, range=(0, 10)))
view(f'Your rating was {stars} stars.')
```
""",
    '### Output',
)


def rating_range(view: View):
    stars = view(*rating_range_docs, box('Rate your experience', mode='rating', value=3, range=(0, 10)))
    view(*rating_range_docs, f'Your rating was {stars} stars.')


topics = dict(
    hello_world=hello_world,
    format_content=format_content,
    format_multiline_content=format_multiline_content,
    display_multiple=display_multiple,
    sequence_views=sequence_views,
    get_input=get_input,
    sequence_inputs=sequence_inputs,
    accept_multiple_inputs=accept_multiple_inputs,
    dunk_your_donuts=dunk_your_donuts,
    markdown_basic=markdown_basic,
    markdown_links=markdown_links,
    markdown_syntax_highlighting=markdown_syntax_highlighting,
    layout_basic=layout_basic,
    layout_row=layout_row,
    layout_col=layout_col,
    layout_size=layout_size,
    layout_gap=layout_gap,
    layout_margin=layout_margin,
    layout_padding=layout_padding,
    layout_background=layout_background,
    layout_color=layout_color,
    layout_border=layout_border,
    layout_align=layout_align,
    layout_tile=layout_tile,
    layout_cross_tile=layout_cross_tile,
    layout_wrap=layout_wrap,
    layout_grow_shrink=layout_grow_shrink,
    form_basic=form_basic,
    form_horizontal=form_horizontal,
    form_combo=form_combo,
    form_improved=form_improved,
    textbox_basic=textbox_basic,
    textbox_label=textbox_label,
    textbox_value=textbox_value,
    textbox_placeholder=textbox_placeholder,
    textbox_required=textbox_required,
    textbox_mask=textbox_mask,
    textbox_icon=textbox_icon,
    textbox_prefix=textbox_prefix,
    textbox_suffix=textbox_suffix,
    textbox_prefix_suffix=textbox_prefix_suffix,
    textbox_error=textbox_error,
    textbox_password=textbox_password,
    textarea=textarea,
    spinbox_basic=spinbox_basic,
    spinbox_value=spinbox_value,
    spinbox_min=spinbox_min,
    spinbox_max=spinbox_max,
    spinbox_step=spinbox_step,
    spinbox_precision=spinbox_precision,
    spinbox_range=spinbox_range,
    spinbox_range_alt=spinbox_range_alt,
    spinbox_range_alt_step=spinbox_range_alt_step,
    spinbox_range_alt_precision=spinbox_range_alt_precision,
    spinbox_negative=spinbox_negative,
    spinbox_decimal_step=spinbox_decimal_step,
    picker_basic=picker_basic,
    picker_buttons=picker_buttons,
    picker_radio=picker_radio,
    picker_dropdown=picker_dropdown,
    picker_multiple_dropdown=picker_multiple_dropdown,
    picker_checklist=picker_checklist,
    picker_dropdown_required=picker_dropdown_required,
    picker_dropdown_error=picker_dropdown_error,
    options_basic=options_basic,
    options_sequence=options_sequence,
    options_string=options_string,
    options_tuples=options_tuples,
    options_dict=options_dict,
    options_selected=options_selected,
    options_value=options_value,
    buttons_basic=buttons_basic,
    buttons_shorthand=buttons_shorthand,
    buttons_selected=buttons_selected,
    buttons_value=buttons_value,
    buttons_values=buttons_values,
    buttons_split=buttons_split,
    buttons_selected_split=buttons_selected_split,
    buttons_caption=buttons_caption,
    buttons_layout=buttons_layout,
    radio_basic=radio_basic,
    radio_value=radio_value,
    radio_selected=radio_selected,
    radio_icon=radio_icon,
    dropdown_basic=dropdown_basic,
    dropdown_value=dropdown_value,
    dropdown_selected=dropdown_selected,
    dropdown_grouped=dropdown_grouped,
    dropdown_editable=dropdown_editable,
    multi_dropdown_basic=multi_dropdown_basic,
    multi_dropdown_value=multi_dropdown_value,
    multi_dropdown_selected=multi_dropdown_selected,
    checklist_basic=checklist_basic,
    checklist_value=checklist_value,
    checklist_selected=checklist_selected,
    slider_basic=slider_basic,
    slider_value=slider_value,
    slider_min=slider_min,
    slider_max=slider_max,
    slider_step=slider_step,
    slider_precision=slider_precision,
    slider_range=slider_range,
    slider_range_alt=slider_range_alt,
    slider_range_alt_step=slider_range_alt_step,
    slider_range_alt_precision=slider_range_alt_precision,
    slider_negative=slider_negative,
    slider_decimal_step=slider_decimal_step,
    range_slider_basic=range_slider_basic,
    range_slider_min=range_slider_min,
    range_slider_max=range_slider_max,
    range_slider_step=range_slider_step,
    range_slider_precision=range_slider_precision,
    range_slider_range=range_slider_range,
    range_slider_range_alt=range_slider_range_alt,
    range_slider_range_alt_step=range_slider_range_alt_step,
    range_slider_range_alt_precision=range_slider_range_alt_precision,
    range_slider_negative=range_slider_negative,
    range_slider_decimal_step=range_slider_decimal_step,
    time_basic=time_basic,
    time_seconds=time_seconds,
    time_hour=time_hour,
    time_24=time_24,
    time_24_seconds=time_24_seconds,
    time_24_hour=time_24_hour,
    date_basic=date_basic,
    date_placeholder=date_placeholder,
    date_required=date_required,
    date_value=date_value,
    date_min=date_min,
    date_max=date_max,
    date_min_max=date_min_max,
    date_range=date_range,
    day_basic=day_basic,
    day_value=day_value,
    day_min=day_min,
    day_max=day_max,
    day_min_max=day_min_max,
    day_range=day_range,
    week_basic=week_basic,
    week_value=week_value,
    week_min=week_min,
    week_max=week_max,
    week_min_max=week_min_max,
    week_range=week_range,
    month_basic=month_basic,
    month_value=month_value,
    month_min=month_min,
    month_max=month_max,
    month_min_max=month_min_max,
    month_range=month_range,
    tag_picker_basic=tag_picker_basic,
    tag_picker_value=tag_picker_value,
    tag_picker_selected=tag_picker_selected,
    color_basic=color_basic,
    color_value=color_value,
    palette_basic=palette_basic,
    palette_value=palette_value,
    palette_selected=palette_selected,
    rating_basic=rating_basic,
    rating_value=rating_value,
    rating_min=rating_min,
    rating_max=rating_max,
    rating_min_max=rating_min_max,
    rating_range=rating_range,
)

table_of_contents = '''
# Welcome to Nitro!

Nitro is the quickest way to build interactive web apps using Python.
No front-end experience required.

This application is a collection of live, annotated examples for how to use
Nitro, and the various features it provides. It acts as a reference for how to
do various things using Nitro, but can also be used as a guide to learn about
many of the features Nitro provides.

## Basics
- [Hello World!](#hello_world)
- [Formatting content](#format_content)
- [Show multiline content](#format_multiline_content)
- [Show items at once](#display_multiple)
- [Show items one at a time](#sequence_views)
- [Get user input](#get_input)
- [Get inputs one at a time](#sequence_inputs)
- [Get inputs at once](#accept_multiple_inputs)
- [Putting it all together](#dunk_your_donuts)
## Markdown
- [Basics](#markdown_basic)
- [Links as inputs](#markdown_links)
- [Syntax highlighting](#markdown_syntax_highlighting)
## Layout
- [Basics](#layout_basic)
- [Rows](#layout_row)
- [Columns](#layout_col)
- [Sizing](#layout_size)
- [Gap](#layout_gap)
- [Margin](#layout_margin)
- [Padding](#layout_padding)
- [Background Color](#layout_background)
- [Text Color](#layout_color)
- [Border Color](#layout_border)
- [Align Text](#layout_align)
- [Tile](#layout_tile)
- [Cross-tile](#layout_cross_tile)
- [Wrap](#layout_wrap)
- [Grow and Shrink](#layout_grow_shrink)
## Forms
- [Basic](#form_basic)
- [Horizontal](#form_horizontal)
- [Combined](#form_combo)
- [Improved](#form_improved)
## Textbox
- [Basic](#textbox_basic)
- [Label](#textbox_label)
- [Value](#textbox_value)
- [Placeholder](#textbox_placeholder)
- [Required](#textbox_required)
- [Input Mask](#textbox_mask)
- [Icon](#textbox_icon)
- [Prefix](#textbox_prefix)
- [Suffix](#textbox_suffix)
- [Prefix and Suffix](#textbox_prefix_suffix)
- [Error](#textbox_error)
- [Password](#textbox_password)
- [Multiple lines](#textarea)
## Spinbox
- [Basic](#spinbox_basic)
- [Value](#spinbox_value)
- [Min](#spinbox_min)
- [Max](#spinbox_max)
- [Step](#spinbox_step)
- [Precision](#spinbox_precision)
- [Min, Max, Step, Precision](#spinbox_range)
- [Range](#spinbox_range_alt)
- [Range with step](#spinbox_range_alt_step)
- [Range with precision](#spinbox_range_alt_precision)
- [Zero-crossing range](#spinbox_negative)
- [Fractional steps](#spinbox_decimal_step)
## Pickers
- [Basic](#picker_basic)
- [Buttons](#picker_buttons)
- [Radio Buttons](#picker_radio)
- [Dropdown](#picker_dropdown)
- [Dropdown List](#picker_multiple_dropdown)
- [Checklist](#picker_checklist)
- [Required](#picker_dropdown_required)
- [Error](#picker_dropdown_error)
## Options
- [Basic](#options_basic)
- [From sequence](#options_sequence)
- [From string](#options_string)
- [From tuples](#options_tuples)
- [From dictionary](#options_dict)
- [Selected](#options_selected)
- [Value](#options_value)
## Buttons
- [Basic](#buttons_basic)
- [Shorthand](#buttons_shorthand)
- [Selected](#buttons_selected)
- [Value](#buttons_value)
- [Values](#buttons_values)
- [Split Buttons](#buttons_split)
- [Primary Split Buttons](#buttons_selected_split)
- [Caption](#buttons_caption)
- [Layout](#buttons_layout)
## Radio Buttons
- [Basic](#radio_basic)
- [Value](#radio_value)
- [Selected](#radio_selected)
- [Icons](#radio_icon)
## Dropdown
- [Basic](#dropdown_basic)
- [Value](#dropdown_value)
- [Selected](#dropdown_selected)
- [Grouped](#dropdown_grouped)
- [Editable](#dropdown_editable)
## Dropdown List
- [Basic](#multi_dropdown_basic)
- [Value](#multi_dropdown_value)
- [Selected](#multi_dropdown_selected)
## Checklist
- [Basic](#checklist_basic)
- [Value](#checklist_value)
- [Selected](#checklist_selected)
## Slider
- [Basic](#slider_basic)
- [Value](#slider_value)
- [Min](#slider_min)
- [Max](#slider_max)
- [Step](#slider_step)
- [Precision](#slider_precision)
- [Min, Max, Step, Precision](#slider_range)
- [Range](#slider_range_alt)
- [Range with step](#slider_range_alt_step)
- [Range with precision](#slider_range_alt_precision)
- [Zero-crossing range](#slider_negative)
- [Fractional steps](#slider_decimal_step)
## Range Slider
- [Basic](#range_slider_basic)
- [Min](#range_slider_min)
- [Max](#range_slider_max)
- [Step](#range_slider_step)
- [Precision](#range_slider_precision)
- [Min, Max, Step, Precision](#range_slider_range)
- [Range](#range_slider_range_alt)
- [Range with step](#range_slider_range_alt_step)
- [Range with precision](#range_slider_range_alt_precision)
- [Zero-crossing range](#range_slider_negative)
- [Fractional steps](#range_slider_decimal_step)
## Time Picker
- [Basic](#time_basic)
- [With seconds](#time_seconds)
- [Hour only](#time_hour)
- [24-hour clock](#time_24)
- [24-hour clock, with seconds](#time_24_seconds)
- [24-hour clock, hour only](#time_24_hour)
## Date Picker
- [Basic](#date_basic)
- [Placeholder](#date_placeholder)
- [Required](#date_required)
- [Value](#date_value)
- [Min](#date_min)
- [Max](#date_max)
- [Min and Max](#date_min_max)
- [Range](#date_range)
## Calendar
- [Basic](#day_basic)
- [Value](#day_value)
- [Min](#day_min)
- [Max](#day_max)
- [Min and Max](#day_min_max)
- [Range](#day_range)
## Week Picker
- [Basic](#week_basic)
- [Value](#week_value)
- [Min](#week_min)
- [Max](#week_max)
- [Min and Max](#week_min_max)
- [Range](#week_range)
## Month Picker
- [Basic](#month_basic)
- [Value](#month_value)
- [Min](#month_min)
- [Max](#month_max)
- [Min and Max](#month_min_max)
- [Range](#month_range)
## Tag Picker
- [Basic](#tag_picker_basic)
- [Value](#tag_picker_value)
- [Selected](#tag_picker_selected)
## Color Picker
- [Basic](#color_basic)
- [Value](#color_value)
## Color Palette
- [Basic](#palette_basic)
- [Value](#palette_value)
- [Selected](#palette_selected)
## Rating
- [Basic](#rating_basic)
- [Value](#rating_value)
- [Min](#rating_min)
- [Max](#rating_max)
- [Min and max](#rating_min_max)
- [Range](#rating_range)
'''


def main(view: View):
    topic = view(table_of_contents)
    topics[topic](view)


nitro = View(
    main,
    title='Nitro',
    caption='v0.1',
    menu=[
        option(main, 'Contents', icon='Documentation'),
        option(main, "Basics", icon="TextDocument", options=[
            option(hello_world, "Hello World!", icon="TextDocument"),
            option(format_content, "Formatting content", icon="TextDocument"),
            option(format_multiline_content, "Show multiline content", icon="TextDocument"),
            option(display_multiple, "Show items at once", icon="TextDocument"),
            option(sequence_views, "Show items one at a time", icon="TextDocument"),
            option(get_input, "Get user input", icon="TextDocument"),
            option(sequence_inputs, "Get inputs one at a time", icon="TextDocument"),
            option(accept_multiple_inputs, "Get inputs at once", icon="TextDocument"),
            option(dunk_your_donuts, "Putting it all together", icon="TextDocument"),
        ]),
        option(main, "Markdown", icon="TextDocument", options=[
            option(markdown_basic, "Basics", icon="TextDocument"),
            option(markdown_links, "Links as inputs", icon="TextDocument"),
            option(markdown_syntax_highlighting, "Syntax highlighting", icon="TextDocument"),
        ]),
        option(main, "Layout", icon="TextDocument", options=[
            option(layout_basic, "Basics", icon="TextDocument"),
            option(layout_row, "Rows", icon="TextDocument"),
            option(layout_col, "Columns", icon="TextDocument"),
            option(layout_size, "Sizing", icon="TextDocument"),
            option(layout_gap, "Gap", icon="TextDocument"),
            option(layout_margin, "Margin", icon="TextDocument"),
            option(layout_padding, "Padding", icon="TextDocument"),
            option(layout_background, "Background Color", icon="TextDocument"),
            option(layout_color, "Text Color", icon="TextDocument"),
            option(layout_border, "Border Color", icon="TextDocument"),
            option(layout_align, "Align Text", icon="TextDocument"),
            option(layout_tile, "Tile", icon="TextDocument"),
            option(layout_cross_tile, "Cross-tile", icon="TextDocument"),
            option(layout_wrap, "Wrap", icon="TextDocument"),
            option(layout_grow_shrink, "Grow and Shrink", icon="TextDocument"),
        ]),
        option(main, "Forms", icon="TextDocument", options=[
            option(form_basic, "Basic", icon="TextDocument"),
            option(form_horizontal, "Horizontal", icon="TextDocument"),
            option(form_combo, "Combined", icon="TextDocument"),
            option(form_improved, "Improved", icon="TextDocument"),
        ]),
        option(main, "Textbox", icon="TextDocument", options=[
            option(textbox_basic, "Basic", icon="TextDocument"),
            option(textbox_label, "Label", icon="TextDocument"),
            option(textbox_value, "Value", icon="TextDocument"),
            option(textbox_placeholder, "Placeholder", icon="TextDocument"),
            option(textbox_required, "Required", icon="TextDocument"),
            option(textbox_mask, "Input Mask", icon="TextDocument"),
            option(textbox_icon, "Icon", icon="TextDocument"),
            option(textbox_prefix, "Prefix", icon="TextDocument"),
            option(textbox_suffix, "Suffix", icon="TextDocument"),
            option(textbox_prefix_suffix, "Prefix and Suffix", icon="TextDocument"),
            option(textbox_error, "Error", icon="TextDocument"),
            option(textbox_password, "Password", icon="TextDocument"),
            option(textarea, "Multiple lines", icon="TextDocument"),
        ]),
        option(main, "Spinbox", icon="TextDocument", options=[
            option(spinbox_basic, "Basic", icon="TextDocument"),
            option(spinbox_value, "Value", icon="TextDocument"),
            option(spinbox_min, "Min", icon="TextDocument"),
            option(spinbox_max, "Max", icon="TextDocument"),
            option(spinbox_step, "Step", icon="TextDocument"),
            option(spinbox_precision, "Precision", icon="TextDocument"),
            option(spinbox_range, "Min, Max, Step, Precision", icon="TextDocument"),
            option(spinbox_range_alt, "Range", icon="TextDocument"),
            option(spinbox_range_alt_step, "Range with step", icon="TextDocument"),
            option(spinbox_range_alt_precision, "Range with precision", icon="TextDocument"),
            option(spinbox_negative, "Zero-crossing range", icon="TextDocument"),
            option(spinbox_decimal_step, "Fractional steps", icon="TextDocument"),
        ]),
        option(main, "Pickers", icon="TextDocument", options=[
            option(picker_basic, "Basic", icon="TextDocument"),
            option(picker_buttons, "Buttons", icon="TextDocument"),
            option(picker_radio, "Radio Buttons", icon="TextDocument"),
            option(picker_dropdown, "Dropdown", icon="TextDocument"),
            option(picker_multiple_dropdown, "Dropdown List", icon="TextDocument"),
            option(picker_checklist, "Checklist", icon="TextDocument"),
            option(picker_dropdown_required, "Required", icon="TextDocument"),
            option(picker_dropdown_error, "Error", icon="TextDocument"),
        ]),
        option(main, "Options", icon="TextDocument", options=[
            option(options_basic, "Basic", icon="TextDocument"),
            option(options_sequence, "From sequence", icon="TextDocument"),
            option(options_string, "From string", icon="TextDocument"),
            option(options_tuples, "From tuples", icon="TextDocument"),
            option(options_dict, "From dictionary", icon="TextDocument"),
            option(options_selected, "Selected", icon="TextDocument"),
            option(options_value, "Value", icon="TextDocument"),
        ]),
        option(main, "Buttons", icon="TextDocument", options=[
            option(buttons_basic, "Basic", icon="TextDocument"),
            option(buttons_shorthand, "Shorthand", icon="TextDocument"),
            option(buttons_selected, "Selected", icon="TextDocument"),
            option(buttons_value, "Value", icon="TextDocument"),
            option(buttons_values, "Values", icon="TextDocument"),
            option(buttons_split, "Split Buttons", icon="TextDocument"),
            option(buttons_selected_split, "Primary Split Buttons", icon="TextDocument"),
            option(buttons_caption, "Caption", icon="TextDocument"),
            option(buttons_layout, "Layout", icon="TextDocument"),
        ]),
        option(main, "Radio Buttons", icon="TextDocument", options=[
            option(radio_basic, "Basic", icon="TextDocument"),
            option(radio_value, "Value", icon="TextDocument"),
            option(radio_selected, "Selected", icon="TextDocument"),
            option(radio_icon, "Icons", icon="TextDocument"),
        ]),
        option(main, "Dropdown", icon="TextDocument", options=[
            option(dropdown_basic, "Basic", icon="TextDocument"),
            option(dropdown_value, "Value", icon="TextDocument"),
            option(dropdown_selected, "Selected", icon="TextDocument"),
            option(dropdown_grouped, "Grouped", icon="TextDocument"),
            option(dropdown_editable, "Editable", icon="TextDocument"),
        ]),
        option(main, "Dropdown List", icon="TextDocument", options=[
            option(multi_dropdown_basic, "Basic", icon="TextDocument"),
            option(multi_dropdown_value, "Value", icon="TextDocument"),
            option(multi_dropdown_selected, "Selected", icon="TextDocument"),
        ]),
        option(main, "Checklist", icon="TextDocument", options=[
            option(checklist_basic, "Basic", icon="TextDocument"),
            option(checklist_value, "Value", icon="TextDocument"),
            option(checklist_selected, "Selected", icon="TextDocument"),
        ]),
        option(main, "Slider", icon="TextDocument", options=[
            option(slider_basic, "Basic", icon="TextDocument"),
            option(slider_value, "Value", icon="TextDocument"),
            option(slider_min, "Min", icon="TextDocument"),
            option(slider_max, "Max", icon="TextDocument"),
            option(slider_step, "Step", icon="TextDocument"),
            option(slider_precision, "Precision", icon="TextDocument"),
            option(slider_range, "Min, Max, Step, Precision", icon="TextDocument"),
            option(slider_range_alt, "Range", icon="TextDocument"),
            option(slider_range_alt_step, "Range with step", icon="TextDocument"),
            option(slider_range_alt_precision, "Range with precision", icon="TextDocument"),
            option(slider_negative, "Zero-crossing range", icon="TextDocument"),
            option(slider_decimal_step, "Fractional steps", icon="TextDocument"),
        ]),
        option(main, "Range Slider", icon="TextDocument", options=[
            option(range_slider_basic, "Basic", icon="TextDocument"),
            option(range_slider_min, "Min", icon="TextDocument"),
            option(range_slider_max, "Max", icon="TextDocument"),
            option(range_slider_step, "Step", icon="TextDocument"),
            option(range_slider_precision, "Precision", icon="TextDocument"),
            option(range_slider_range, "Min, Max, Step, Precision", icon="TextDocument"),
            option(range_slider_range_alt, "Range", icon="TextDocument"),
            option(range_slider_range_alt_step, "Range with step", icon="TextDocument"),
            option(range_slider_range_alt_precision, "Range with precision", icon="TextDocument"),
            option(range_slider_negative, "Zero-crossing range", icon="TextDocument"),
            option(range_slider_decimal_step, "Fractional steps", icon="TextDocument"),
        ]),
        option(main, "Time Picker", icon="TextDocument", options=[
            option(time_basic, "Basic", icon="TextDocument"),
            option(time_seconds, "With seconds", icon="TextDocument"),
            option(time_hour, "Hour only", icon="TextDocument"),
            option(time_24, "24-hour clock", icon="TextDocument"),
            option(time_24_seconds, "24-hour clock, with seconds", icon="TextDocument"),
            option(time_24_hour, "24-hour clock, hour only", icon="TextDocument"),
        ]),
        option(main, "Date Picker", icon="TextDocument", options=[
            option(date_basic, "Basic", icon="TextDocument"),
            option(date_placeholder, "Placeholder", icon="TextDocument"),
            option(date_required, "Required", icon="TextDocument"),
            option(date_value, "Value", icon="TextDocument"),
            option(date_min, "Min", icon="TextDocument"),
            option(date_max, "Max", icon="TextDocument"),
            option(date_min_max, "Min and Max", icon="TextDocument"),
            option(date_range, "Range", icon="TextDocument"),
        ]),
        option(main, "Calendar", icon="TextDocument", options=[
            option(day_basic, "Basic", icon="TextDocument"),
            option(day_value, "Value", icon="TextDocument"),
            option(day_min, "Min", icon="TextDocument"),
            option(day_max, "Max", icon="TextDocument"),
            option(day_min_max, "Min and Max", icon="TextDocument"),
            option(day_range, "Range", icon="TextDocument"),
        ]),
        option(main, "Week Picker", icon="TextDocument", options=[
            option(week_basic, "Basic", icon="TextDocument"),
            option(week_value, "Value", icon="TextDocument"),
            option(week_min, "Min", icon="TextDocument"),
            option(week_max, "Max", icon="TextDocument"),
            option(week_min_max, "Min and Max", icon="TextDocument"),
            option(week_range, "Range", icon="TextDocument"),
        ]),
        option(main, "Month Picker", icon="TextDocument", options=[
            option(month_basic, "Basic", icon="TextDocument"),
            option(month_value, "Value", icon="TextDocument"),
            option(month_min, "Min", icon="TextDocument"),
            option(month_max, "Max", icon="TextDocument"),
            option(month_min_max, "Min and Max", icon="TextDocument"),
            option(month_range, "Range", icon="TextDocument"),
        ]),
        option(main, "Tag Picker", icon="TextDocument", options=[
            option(tag_picker_basic, "Basic", icon="TextDocument"),
            option(tag_picker_value, "Value", icon="TextDocument"),
            option(tag_picker_selected, "Selected", icon="TextDocument"),
        ]),
        option(main, "Color Picker", icon="TextDocument", options=[
            option(color_basic, "Basic", icon="TextDocument"),
            option(color_value, "Value", icon="TextDocument"),
        ]),
        option(main, "Color Palette", icon="TextDocument", options=[
            option(palette_basic, "Basic", icon="TextDocument"),
            option(palette_value, "Value", icon="TextDocument"),
            option(palette_selected, "Selected", icon="TextDocument"),
        ]),
        option(main, "Rating", icon="TextDocument", options=[
            option(rating_basic, "Basic", icon="TextDocument"),
            option(rating_value, "Value", icon="TextDocument"),
            option(rating_min, "Min", icon="TextDocument"),
            option(rating_max, "Max", icon="TextDocument"),
            option(rating_min_max, "Min and max", icon="TextDocument"),
            option(rating_range, "Range", icon="TextDocument"),
        ]),
    ],
    nav=[
        option(main, 'Contents'),
    ],
)

app = Flask(__name__, static_folder=web_directory, static_url_path='')


@app.route('/')
def home_page():
    return send_from_directory(web_directory, 'index.html')


@app.route('/nitro', websocket=True)
def socket():
    ws = simple_websocket.Server(request.environ)
    try:
        nitro.serve(ws.send, ws.receive)
    except simple_websocket.ConnectionClosed:
        pass
    return ''


if __name__ == '__main__':
    app.run()
