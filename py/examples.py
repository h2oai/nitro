# Copyright 2022 H2O.ai, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from h2o_nitro import View, box, row, col, option, lorem


# # Basics

# ## Hello World!
# Call `view()` to show something on a page.
def hello_world(view: View):
    view('Hello World!')


# Here, `view()` is comparable to Python's built-in `print()` function,
# and prints its arguments to the web page.

# ## Formatting content
# Strings passed to `view()` are interpreted as
# [Markdown](https://github.github.com/gfm/)
def format_content(view: View):
    view('_Less_ `code` means _less_ **bugs**.')


# ## Show multiline content
# Triple-quote strings to pass multiple lines of markdown.
def format_multiline_content(view: View):
    view('''
    The King said, very gravely:
    - Begin at the beginning,
    - And go on till you come to the end,
    - Then stop.
    ''')


# ## Show items at once
# Pass multiple arguments to `view()` to lay them out top to bottom.
def display_multiple(view: View):
    view(
        'Begin at the beginning,',
        'And go on till you come to the end,',
        'Then stop.',
    )


# ## Show items one at a time
# Call `view()` multiple times to show items one at a time.
#
# The following example steps through three different pages.
def sequence_views(view: View):
    view('Begin at the beginning,')
    view('And go on till you come to the end,')
    view('Then stop.')


# ## Style text
# To style text, put it in a `box()`, and style the box.
#
# `view(text)` is in fact shorthand for `view(box(text))`.
def style_text(view: View):
    view(
        box('Hello World!', color='red', border='red'),
        box('Hello World!', color='white', background='red'),
        box('Hello World!', width='50%', background='#eee'),
    )


# In general, `box()` can be used to create all kinds of content, like text blocks, dropdowns,
# spinboxes, checklists, buttons, calendars, and so on.

# ## Get user input
# Call `box()` with `value=` to create an input field and pass it to `view()`.
#
# When a view contains an input field, the `view()` function returns its input value.
#
def get_input(view: View):
    # Display a textbox and assign the entered value to a variable.
    name = view(box('What is your name?', value='Boaty McBoatface'))
    # Print the entered value.
    view(f'Hello, {name}!')


# Here, `view(box())` behaves similar to Python's built-in `input()` function.
#

# ## Get inputs one at a time
# Call `view()` multiple times to prompt for a sequence of inputs, one at a time.
#
# The following example steps through three different pages.
def sequence_inputs(view: View):
    # Prompt for first name.
    first_name = view(box('First name', value='Boaty'))
    # Prompt for last name.
    last_name = view(box('Last name', value='McBoatface'))
    # Print the entered values.
    view(f'Hello, {first_name} {last_name}!')


# ## Get inputs at once
# Pass multiple boxes to `view()` to prompt for inputs at once.
#
# When a view contains multiple boxes, the `view()` function returns multiple values, in order.
def accept_multiple_inputs(view: View):
    # Prompt for first and last names.
    first_name, last_name = view(
        box('First name', value='Boaty'),
        box('Last name', value='McBoatface'),
    )
    # Print the entered values
    view(f'Hello, {first_name} {last_name}!')


# ## Putting it all together
# Views can be chained together to create sophisticated workflows and wizards.
#
# The example below shows a simple online ordering system.
#
# Observe how it combines `view()` with conditionals and loops, while keeping the code
# simple, concise, and clear.
#
# Notably, if you have built web applications before, notice the absence of callbacks, event handlers,
# web request handlers, routing, etc.
def dunk_your_donuts(view: View):
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


# Building a similar multi-page interactive app with a regular web framework can be
# a fairly complex endeavor, weaving together requests and replies with logic spread across
# multiple functions , but Nitro makes all this delightfully simple!

# # Markdown

# ## Basics
# Strings passed to `view()` are interpreted as [Github Flavored Markdown](https://github.github.com/gfm/) (GFM).
#
# `view(text)` is shorthand for `view(box(text))`.
def markdown_basic(view: View):
    view('''
    # Heading 1
    ## Heading 2
    ### Heading 3 
    #### Heading 4
    ##### Heading 5 
    ###### Heading 6

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


# Any uniform indentation is automatically ignored.

# ## Links as inputs
# Local links in markdown content behave just like any other input.
#
# Clicking on a local link returns the name of the link.
def markdown_links(view: View):
    choice = view('''
    Pick a flavor:
    - [Vanilla](#vanilla)
    - [Strawberry](#strawberry)
    - [Chocolate](#chocolate)

    Or, [surprise me](#surprise-me)!
    ''')
    view(f'You clicked on {choice}.')


# ## Tables
# Draw tables using `---` and `|`.
#
# - Use three or more hyphens (`---`) to create each column’s header.
# - Use `|` to separate each column.
# - Use `:---` to left-align text.
# - Use `:---:` to center text.
# - Use `---:` to right-align text.
def markdown_table(view: View):
    view('''
    
    ### Basic Tables
    
    | Flavor         | Super cheap! |
    | -------------- | ------------ |
    | Cinnamon Sugar | $1.99        |
    | Powdered Sugar | $1.99        |
    | Vanilla        | $2.99        |
    | Chocolate      | $2.99        |
    | Blueberry      | $2.99        |
    
    ### Column alignment
    
    | Flavor         | Super cheap! | Extras                |
    | -------------: | :----------: | :-------------------- |
    | Cinnamon Sugar | $1.99        | Sugar and spice.      |
    | Powdered Sugar | $1.99        | Served warm.          |
    | Vanilla        | $2.99        | With cookie crumbles. |
    | Chocolate      | $2.99        | With sprinkles.       |
    | Blueberry      | $2.99        | With real blueberry.  |
    
    ''')


# ## Tables from lists
# It's often easier to construct tables from lists of things, as shown below.
def show_table(view: View):
    view(make_table([
        ['Flavor', 'Super cheap!'],
        ['Cinnamon Sugar', '$1.99'],
        ['Powdered Sugar', '$1.99'],
        ['Vanilla', '$2.99'],
        ['Chocolate', '$2.99'],
        ['Blueberry', '$2.99'],
    ]))


def make_table_row(row):
    return f"| {' | '.join(row)} |"


def make_table(rows):
    rows = [rows[0], ['---'] * len(rows[0]), *rows[1:]]
    return '\n'.join([make_table_row(row) for row in rows])


# ## Syntax highlighting
# Code blocks in Markdown support syntax highlighting for 180+ languages using [highlight.js](https://highlightjs.org/).
#
# To enable syntax highlighting, suffix the language to the opening triple-backticks.
#
# [See list of supported languages](https://github.com/highlightjs/highlight.js/blob/main/SUPPORTED_LANGUAGES.md).
def markdown_syntax_highlighting(view: View):
    view('''
    Python:
    ```py
    def hello():
        print('Hello!')
    ```
    
    Ruby:
    ```rb
    def hello
        puts "Hello!"
    end
    ```

    Javascript:
    ```js
    function hello() {
        console.log('Hello!');
    }
    ```
    ''')


# # Styling

# ## Background Color
# Set `background=` to apply a background color.
#
# The text color is automatically changed to a contrasting color if not specified.
# A `10px` padding is automatically applied if not specified.
def styling_background(view: View):
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


# ## Text Color
# Set `color=` to change the text color.
def styling_color(view: View):
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    '''
    view(
        box(text, color='#e63946'),
        box(text, color='#457b9d'),
        box(text, color='#1d3557'),
    )


# ## Border Color
# Set `border=` to add a border.
#
# A `10px` padding is automatically applied if not specified.
def styling_border(view: View):
    text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed 
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    '''
    view(
        box(text, border='#e63946'),
        box(text, border='#457b9d'),
        box(text, border='#1d3557'),
    )


# ## Align Text
# Set `align=` to `left`, `right`, `center` or `justify` to align text.
def styling_align(view: View):
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


# ## Sizing
# Nitro provides extensive control over how items are sized and spaced, using `width`, `height`, `margin`, `padding`,
# and `gap`.
#
# These parameters can be specified as either integers or strings.
#
# - Integers are interpreted as pixels, e.g. `42` and `'42px'` have the same effect.
# - Strings must be a number followed by one of the units listed below (e.g. `'42px'`, `'42in'`, `'42mm'`, etc.
#   - Absolute units:
#     - `px`: One pixel (1/96th of an inch).
#     - `cm`: One centimeter.
#     - `mm`: One millimeter.
#     - `in`: One inch (96px).
#     - `pc`: One pica (12pt or 1/6th of an inch).
#     - `pt`: One point (1/72nd of an inch).
#   - Relative units:
#     - `%`: A percentage of the container's size.
#     - `vh`: 1% of the viewport height.
#     - `vw`: 1% of the viewport width.
#     - `vmin`: The smaller of `vw` and `vh`.
#     - `vmax`: The larger of `vw` and `vh`.
#     - `ex`: The x-height of the font of the element.
#     - `em`: The font size of the element.
#     - `rem`: The font size of the page.

def styling_size(view: View):
    text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    view(
        box(text, width=200, background='#eee'),  # interpreted as '200px'
        box(text, width='250px', background='#eee'),
        box(text, width='3in', background='#eee'),
        box(text, width='50%', background='#eee'),
        box(text, height='1in', background='#eee'),
        box(text, width='250px', height='100px', background='#eee'),
    )


# ## Margin
# Set `margin=` to add a margin around each item.
#
# Top, right, bottom, left margins can be controlled independently, and are specified
# as `'top right bottom left'` strings.
#
# - `'x'` is shorthand for `'x x x x'`.
# - `'x y'` is shorthand for `'x y x y'`.
# - `'x y z'` is shorthand for `'x y z y'`.
def styling_margin(view: View):
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


# ## Padding
# Set `padding=` to control the padding (inset) inside each item.
#
# Top, right, bottom, left paddings can be controlled independently, and are specified
# as `'top right bottom left'` strings.
#
# - `'x'` is shorthand for `'x x x x'`.
# - `'x y'` is shorthand for `'x y x y'`.
# - `'x y z'` is shorthand for `'x y z y'`.
def styling_padding(view: View):
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


# # Images

# ## Basic
# Set `image=` to display an image.
def image_basic(view: View):
    view(box(image='sample.jpg'))


# ## Resize
# Images can be resized by setting `width=` or `height=` or both.
#
# - If only `width=` or only `height=` are set, the image is scaled proportionally.
# - If both `width=`and`height=`are set, the image is stretched to fit, and might appear distorted.
def image_resize(view: View):
    view(
        box(image='sample.jpg', width=300),
        box(image='sample.jpg', height=200),
        box(image='sample.jpg', width=150, height=300),
    )


# ## Fit
# Set `fit=` to control how the image should be resized to fit its box.
#
# - `fit='cover'` (default) scales and *clips* the image while preserving its aspect ratio.
# - `fit='contain'` scales and *letterboxes* the image while preserving its aspect ratio.
# - `fit='fill'` stretches the image to fit.
# - `fit='none'` clips the image without resizing.
# - `fit='scale-down'` behaves like either `contain` or `none`, whichever results in a smaller image.
def image_fit(view: View):
    style = dict(width=100, height=200)
    view(
        row(
            box(image='sample.jpg', fit='cover', **style),
            box(image='sample.jpg', fit='contain', **style),
            box(image='sample.jpg', fit='fill', **style),
            box(image='sample.jpg', fit='none', **style),
            box(image='sample.jpg', fit='scale-down', **style),
        )
    )


# ## Backdrop
# If a box contains content, its image is used as a backdrop.
#
# Set `fit=` to control how the backdrop should be resized to fit the box.
def image_background(view: View):
    style = dict(width=100, height=200, color='white')
    view(
        row(
            box('Astro', image='sample.jpg', **style),
            box('Astro', image='sample.jpg', fit='cover', **style),
            box('Astro', image='sample.jpg', fit='contain', **style),
            box('Astro', image='sample.jpg', fit='fill', **style),
            box('Astro', image='sample.jpg', fit='none', **style),
            image='sample.jpg',  # A backdrop for the row as well!
        )
    )


# # Layout

# ## Basics
# By default each item passed to `view()` are laid out one below the other, with a 10px gap.
def layout_basic(view: View):
    view(
        box(value='Top'),
        box(value='Middle'),
        box(value='Bottom'),
    )


# ## Rows
# Use `row()` to lay out multiple items horizontally, left to right.
#
# By default, items take up equal amounts of space, with a `10px` gap between the items.
def layout_row(view: View):
    view(row(
        box(value='Left'),
        box(value='Center'),
        box(value='Right'),
    ))


# Setting `row=True` produces the same result as wrapping items with `row()`.
def layout_row_alt(view: View):
    view(
        box(value='Left'),
        box(value='Center'),
        box(value='Right'),
        row=True,
    )


# ## Columns
# Use `col()` to lay out multiple items vertically, top to bottom.
#
# The example shows one row split into three columns containing three rows each.
def layout_col(view: View):
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


# ## Tile
# Set `tile=` to control how items inside a view, row, or column are tiled along the main axis.
#
# - The main axis for a row is horizontal, starting at the left, and ending at the right.
# - The main axis for a column is vertical, starting at the top, and ending at the bottom
#
# `tile=` can be set to `start`, `center`, `end`, `between`, `around`, `evenly`, `stretch`, or `normal`.
def layout_tile(view: View):
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


# ## Cross Tile
# Set `cross_tile=` to control how items inside a view, row, or column are tiled along the cross axis.
#
# - The cross axis for a row is vertical. starting at the top, and ending at the bottom
# - The cross axis for a column is horizontal, starting at the left, and ending at the right.
#
# `cross_tile=` can be set to `start`, `center`, `end`, `stretch`, or `normal`.
def layout_cross_tile(view: View):
    boxes = [box(text=f'{i + 1}', background='#666', width=100) for i in range(3)]
    col_style = dict(height=200, background='#eee')
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


# ## Gap
# Set `gap=` to control the spacing between items. The default gap is `10` or `'10px'`.
def layout_gap(view: View):
    view(
        box(value='Top'),
        box(value='Middle'),
        box(value='Bottom'),
        gap=25,
    )


# ## Wrap
# Set `wrap=` to control how items are wrapped inside a view, row, or column.
#
# `wrap=` can be set to `start`, `center`, `end`, `between`, `around`, `evenly`, `stretch`, or `normal`.
def layout_wrap(view: View):
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


# ## Grow and Shrink
# Set `grow=` or `shrink=` to specify what amount of the available space the item should take up
# inside a view, row, or column.
#
# Setting `grow=` expands the item. Setting `shrink=` contracts the item. Both are proportions.
#
# By default, items are grown or shrunk based on their initial size. To resize them on a different basis,
# set `basis=` to the value you want.
#
# - `basis=0` means "distribute available space assuming that the initial size is zero".
# - `basis='20px'` means "distribute available space assuming that the initial size is 20px".
# - The default behavior (if `basis=` is not set) is to assume that the initial size is the size of the item's content.
def layout_grow_shrink(view: View):
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


# ## Vertical Alignment
# Use `tile='center'` to center content vertically inside a box.
#
# The following example centers content both horizontally and vertically.
def layout_vertical_alignment(view: View):
    view(
        box(
            '# Donuts',
            tile='center', cross_tile='center',
            height='300px', background='$foreground', color='$background',
        )
    )


# # Forms

# ## Basic
# To create a form, simply lay out all the inputs you need inside a view, then destructure the return value in order.
def form_basic(view: View):
    username, password, action = view(
        box('Username', value='someone@company.com'),
        box('Password', value='pa55w0rd', password=True),
        box(['Login']),
    )
    view(f'You entered `{username}`/`{password}` and then clicked on {action}.')


# ## Horizontal
# Wrap items with `row()` to lay them out left to right.
# There is no change to the way the return values are destructured.
def form_horizontal(view: View):
    username, password, action = view(
        row(
            box('Username', value='someone@company.com'),
            box('Password', value='pa55w0rd', password=True),
            box(['Login']),
        )
    )
    view(f'You entered `{username}`/`{password}` and then clicked on {action}.')


# ## Combined
# Use `row()` and `col()` to mix and match how items are laid out. Destructure the return values in the same order.
def form_combo(view: View):
    first, last, addr1, addr2, city, state, zip, action = view(
        row(box('First name', value=''), box('Last name', value='')),
        box('Address line 1', value=''),
        box('Address line 2', value=''),
        row(box('City', value=''), box('State', value=''), box('Zip', value='')),
        box([
            option('yes', 'Sign me up!'),
            option('no', 'Not now'),
        ])
    )
    view(f'''
    You provided:
    
    Address: {first} {last}, {addr1}, {addr2}, {city} {state} {zip}
    
    Sign up: {action}
    ''')


# ## Improved
# Specify additional layout parameters like `width=`, `grow=`, etc. to get more control over
# how items are laid out.
def form_improved(view: View):
    first, middle, last, addr1, addr2, city, state, zip, action = view(
        row(box('First name', value=''), box('M.I.', value='', width='10%'), box('Last name', value='')),
        box('Address line 1', value=''),
        box('Address line 2', value=''),
        row(box('City', value='', grow=5), box('State', value='', width='20%'), box('Zip', value='', grow=1)),
        box([
            option('yes', 'Sign me up!', caption='Terms and conditions apply'),
            option('no', 'Not now', caption="I'll decide later"),
        ])
    )
    view(f'''
    You provided:

    Address: {first} {middle} {last}, {addr1}, {addr2}, {city} {state} {zip}

    Sign up: {action}
    ''')


# # Textbox

# ## Basic
# Call `box()` with `mode='text'` to show a textbox.
#
# The return value is the text entered into the box.
def textbox_basic(view: View):
    x = view(box(mode='text'))
    view(f'You entered {x}.')


# ## Value
# Set `value=` to prefill the box with a value.
#
# `mode='text'` can be elided if `value=` is set.
def textbox_value(view: View):
    speed = view(box(value='60 km/h'))
    view(f'Your speed is {speed} km/h.')


# ## Label
# Any text passed to `box()` is used as a label.
def textbox_label(view: View):
    speed = view(box('Speed', value='60'))
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
#
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

# # Spinbox

# ## Basic
# Call `box()` with `mode='number'` to show a box with increment/decrement buttons.
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
#
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


# # Checkbox

# ## Basic
# Set `mode='check'` to show a checkbox.
def checkbox_basic(view: View):
    keep_signed_in = view(box('Keep me signed in', mode='check'))
    view(f'Keep me signed in: {keep_signed_in}.')


# ## Value
# Set `value=True` to pre-select the checkbox.
#
# The mode setting `mode='check'` is implied, and can be elided.
def checkbox_value(view: View):
    keep_signed_in = view(box('Keep me signed in', value=True))
    view(f'Keep me signed in: {keep_signed_in}.')


# # Pickers

# ## Basic
# A *picker* is a box that allows the user to pick one or more options from several presented options, like buttons,
# checklists, dropdowns, color pickers, and so on.
#
# Set `options=` to create a picker.
def picker_basic(view: View):
    choice = view(box('Choose a color', options=[
        'green', 'yellow', 'orange', 'red'
    ]))
    view(f'You chose {choice}.')


# There are several ways to create options. These are explained in the next section. The simplest way is to supply a
# sequence (tuple, set or list) of strings.
#
# By default, this shows buttons for up to 3 options, radio buttons for up to 7 options,
# or a dropdown menu for more than 7 options.
# This behavior can be controlled using `mode=`, explained in later examples.
#
# The example above has 4 options, hence radio buttons are shown.


# ## Buttons
# Buttons are shown for up to 3 options.
#
# Set `mode='button'` to display buttons regardless of the number of options.
def picker_buttons(view: View):
    choice = view(box('Choose a color', options=[
        'yellow', 'orange', 'red'
    ]))
    view(f'You chose {choice}.')


# ## Radio Buttons
# Radio buttons is shown for 4-7 options.
#
# Set `mode='radio'` to display radio buttons regardless of the number of options.
def picker_radio(view: View):
    choice = view(box('Choose a color', options=[
        'green', 'yellow', 'orange', 'red'
    ]))
    view(f'You chose {choice}.')


# ## Dropdown
# A dropdown menu is shown for more than 7 options.
#
# Set `mode='menu'` to display a dropdown menu regardless of the number of options.
def picker_dropdown(view: View):
    choice = view(box('Choose a color', options=[
        'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Dropdown List
# Set `multiple=True` to allow choosing more than one option. The return value is a list of choices made.
#
# By default, this displays checkboxes for up to 7 options, or a dropdown menu for more than 7 options.
#
# Set `mode='menu'` to display a dropdown menu regardless of the number of options.
def picker_multiple_dropdown(view: View):
    choices = view(box('Choose some colors', multiple=True, options=[
        'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choices}.')


# ## Checklist
# A checklist is shown for up to 7 options when `multiple=True`.
#
# Set `mode='check'` to display a checklist regardless of the number of options.
def picker_checklist(view: View):
    choices = view(box('Choose some colors', mode='check', multiple=True, options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choices}.')


# ## Required
# Set `required=True` to indicate that input is required.
def picker_dropdown_required(view: View):
    choice = view(box('Choose a color', mode='menu', required=True, options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Error
# Set `error=` to show an error message below the box.
def picker_dropdown_error(view: View):
    choice = view(box('Choose a color', mode='menu', error='Invalid input', options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# # Options

# ## Basic
# An `option` represents one of several choices to be presented to the user.
# It's used by all kinds of pickers: buttons, dropdowns, checklists, color pickers, and so on.
#
# An option has a `value` and `text`, created using `option(value, text)`.
#
# - The `value` is the value returned when the user picks that option. It is not user-visible.
# - The `text` is typically used as a label for the option.
#
# If `text` is not provided, then the `value` is also used as the `text`.
#
# There are other, more concise ways to specify options, explained in later examples.
def options_basic(view: View):
    choice = view(box('Choose a color', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# ## From sequence
# If `options` is a sequence (tuple, set or list), the elements of the sequence are used as options.
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


# In other words, `'green yellow orange red'` is shorthand for `['green', 'yellow', 'orange', 'red']`.

# ## From tuples
# `options=` can also be specified as a sequence of `(value, text)` tuples.
def options_tuples(view: View):
    choice = view(box('Choose a color', options=[
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('orange', 'Orange'),
        ('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# Here, `(value, text)` is shorthand for `option(value, text)`.

# ## From dictionary
# `options=` can also be specified as a `dict` of `value: text` entries.
def options_dict(view: View):
    choice = view(box('Choose a color', options=dict(
        green='Green',
        yellow='Yellow',
        orange='Orange',
        red='Red',
    )))
    view(f'You chose {choice}.')


# This is the most concise way to pass options where labels differ from values.

# ## Selected
# Set `selected=True` to pre-select an option.
#
# Another way to pre-select an option is to set `value=` on the box, as shown in the next example.
def options_selected(view: View):
    choice = view(box('Choose a color', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# ## Value
# Set `value=` on the box to pre-select an option having that value.
#
# Another way to pre-select an option is to set `selected=True` on the option, as shown in the previous example.
def options_value(view: View):
    choice = view(box('Choose a color', value='yellow', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# # Buttons

# ## Basic
# Set `mode='button'` to show buttons.
#
# `mode=` can be elided when there are 1-3 options.
def buttons_basic(view: View):
    choice = view(box('Choose a color', mode='button', options=[
        'auto', 'yellow', 'orange', 'red',
    ]))
    view(f'You chose {choice}.')


# ## Shorthand
# Most often, it doesn't make sense to show a text prompt above a set of buttons.
#
# In such cases, `box(mode='button', options=X)` can be shortened to `box(X)`.
#
# In other words, if the first argument to `box()` is a sequence of options, then `mode='button'` is implied.
def buttons_shorthand(view: View):
    # Longer
    choice = view(box(mode='button', options=['auto', 'yellow', 'orange', 'red']))

    # Shorter
    choice = view(box(['auto', 'yellow', 'orange', 'red']))

    view(f'You chose {choice}.')


# `options` can be a sequence of options, a sequence of tuples, or a dictionary. The following forms are equivalent:
def buttons_shorthand_alt(view: View):
    # Longer
    choice = view(box([
        option('auto', 'Automatic'),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))

    # Shorter
    choice = view(box([
        ('auto', 'Automatic'),
        ('yellow', 'Yellow'),
        ('orange', 'Orange'),
        ('red', 'Red'),
    ]))

    # Shortest
    choice = view(box(dict(
        auto='Automatic',
        yellow='Yellow',
        orange='Orange',
        red='Red',
    )))


# ## Selected
# By default, the first button is displayed as the primary action in the sequence.
#
# To select a different button as primary, set `selected=True`.
def buttons_selected(view: View):
    choice = view(
        'Updates are available!',
        box([
            option('now', 'Update now'),
            option('tomorrow', 'Remind me tomorrow', selected=True),
            option('never', 'Never update'),
        ])
    )
    view(f'You chose to update {choice}.')


# ## Value
# Alternatively, Set `value=` to mark a button as *primary*.
def buttons_value(view: View):
    choice = view(
        'Updates are available!',
        box(dict(
            now='Update now',
            tomorrow='Remind me tomorrow',
            never='Never update',
        ), value='now')
    )
    view(f'You chose to update {choice}.')


# ## Values
# If `value=` is set to a sequence, all buttons with those values are marked as *primary*.
def buttons_values(view: View):
    choice = view(
        'Sign me up!',
        box(dict(
            basic='Basic Plan ($9.99/month)',
            pro='Pro Plan ($14.99/month)',
            none='Not interested',
        ), value=['basic', 'pro'])
    )
    view(f'You chose {choice}.')


# ## Split Buttons
# Sub-options inside options are shown as split buttons.
def buttons_split(view: View):
    choice = view(
        'Send fresh donuts every day?',
        box([
            option('yes', 'Yes!'),
            option('no', 'No', options=[
                option('later', 'Remind me later', icon='ChatBot'),
                option('never', "Don't ask me again", icon='MuteChat'),
            ]),
        ])
    )
    view(f'You chose {choice}.')


# ## Primary Split Buttons
# Sub-options work for primary buttons, too.
def buttons_selected_split(view: View):
    choice = view(
        'Send fresh donuts every day?',
        box([
            option('yes', 'Yes!', options=[
                option('later', 'Remind me later', icon='ChatBot'),
                option('never', "Don't ask me again", icon='MuteChat'),
            ]),
            option('no', 'No'),
        ])
    )
    view(f'You chose {choice}.')


# ## Caption
# Set `caption=` to describe buttons.
def buttons_caption(view: View):
    choice = view(
        'Send fresh donuts every day?',
        box([
            option('yes', 'Sign me up!', caption='Terms and conditions apply'),
            option('no', 'Not now', caption='I will decide later'),
        ])
    )
    view(f'You chose {choice}.')


# ## Layout
# By default, buttons are arranged row-wise. Set `row=False` to arrange them column-wise.
def buttons_layout(view: View):
    choice = view(
        'Choose a color:',
        box([
            option('auto', 'Automatic'),
            option('yellow', 'Yellow'),
            option('orange', 'Orange'),
            option('red', 'Red'),
        ], row=False)
    )
    view(f'You chose {choice}.')


# # Radio Buttons

# ## Basic
# Set `mode='radio'` to show radio buttons.
#
# `mode=` can be elided when there are 4-7 options.
def radio_basic(view: View):
    choice = view(box('Choose a color', mode='radio', options=[
        'blue', 'green', 'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Value
# Set `value=` to pre-select an option having that value.
def radio_value(view: View):
    choice = view(box('Choose a color', mode='radio', value='yellow', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# ## Selected
# Set `selected=True` to pre-select an option.
def radio_selected(view: View):
    choice = view(box('Choose a color', mode='radio', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# ## Icons
# Set `icon=` to show graphical options.
def radio_icon(view: View):
    choice = view(box('Choose a chart type', mode='radio', options=[
        option('area', 'Area', icon='AreaChart', selected=True),
        option('bar', 'Bar', icon='BarChartHorizontal'),
        option('column', 'Column', icon='BarChartVertical'),
        option('line', 'Line', icon='LineChart'),
        option('scatter', 'Scatter', icon='ScatterChart'),
        option('donut', 'Donut', icon='DonutChart'),
    ]))
    view(f'You chose {choice}.')


# # Dropdown

# ## Basic
# Set `mode='menu'` to show a dropdown menu.
#
# `mode=` can be elided when there are more than 7 options.
def dropdown_basic(view: View):
    choice = view(box('Choose a color', mode='menu', options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Value
# Set `value=` to pre-select an option having that value.
def dropdown_value(view: View):
    choice = view(box('Choose a color', mode='menu', value='yellow', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# ## Selected
# Set `selected=True` to pre-select an option.
def dropdown_selected(view: View):
    choice = view(box('Choose a color', mode='menu', options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ]))
    view(f'You chose {choice}.')


# ## Grouped
# Options can have sub-options. This is useful for grouping options into categories.
#
# `mode=menu` is implied if options are grouped.
def dropdown_grouped(view: View):
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


# ## Editable
# Set `editable=True` to allow arbitrary input in addition to the presented options.
#
# `mode=menu` is implied if `editable=True`.
def dropdown_editable(view: View):
    choice = view(box('Choose a color', editable=True, options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# # Dropdown List

# ## Basic
# Set `mode='menu'` with `multiple=True` to show a dropdown menu that allows multiple options to be selected.
#
# `mode=` can be elided when there are more than 7 options.
def multi_dropdown_basic(view: View):
    choices = view(box(
        'Choose some colors',
        mode='menu',
        multiple=True,
        options=['green', 'yellow', 'orange', 'red']
    ))
    view(f'You chose {choices}.')


# ## Value
# Set `value=` to pre-select options having those values.
def multi_dropdown_value(view: View):
    choices = view(box(
        'Choose some colors',
        mode='menu',
        multiple=True,
        value=['yellow', 'red'],
        options=['green', 'yellow', 'orange', 'red']
    ))
    view(f'You chose {choices}.')


# ## Selected
# Alternatively, set `selected=True` to pre-select one or more options.
def multi_dropdown_selected(view: View):
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


# # Checklist

# ## Basic
# Set `mode='check'` to show a checklist
#
# `mode=` can be elided when there are 1-7 options.
def checklist_basic(view: View):
    choices = view(box(
        'Choose some colors',
        mode='check',
        options=['green', 'yellow', 'orange', 'red']
    ))
    view(f'You chose {choices}.')


# ## Value
# Set `value=` to pre-select options having those values.
def checklist_value(view: View):
    choices = view(box(
        'Choose some colors',
        mode='check',
        value=['yellow', 'red'],
        options=['green', 'yellow', 'orange', 'red']
    ))
    view(f'You chose {choices}.')


# ## Selected
# Alternatively, set `selected=True` to pre-select one or more options.
def checklist_selected(view: View):
    choices = view(box(
        'Choose some colors',
        mode='check',
        options=[
            option('green', 'Green'),
            option('yellow', 'Yellow', selected=True),
            option('orange', 'Orange'),
            option('red', 'Red', selected=True),
        ]
    ))
    view(f'You chose {choices}.')


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
#
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
# Setting `range=` to a `(min, max, step, precision)` tuple is shorthand setting
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
# Setting `range=` to a `(min, max, step, precision)` tuple is shorthand for setting
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
# Exclude `AM` or `PM` from the `value` to accept input in military time.
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
#
# Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
# Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.
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
#
# Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
# Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.
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
#
# Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
# Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.
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


# # Tag Picker

# ## Basic
# Set `mode='tag'` to display a tag picker. `multiple=True` is implied.
def tag_picker_basic(view: View):
    tags = view(box(
        'Choose some tags',
        mode='tag',
        options=['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']
    ))
    view(f'You chose {tags}.')


# ## Value
# Set `value=` to pre-select options having those values.
def tag_picker_value(view: View):
    tags = view(box(
        'Choose some tags',
        mode='tag',
        value=['yellow', 'red'],
        options=['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']
    ))
    view(f'You chose {tags}.')


# ## Selected
# Set `selected=True` to pre-select one or more options.
def tag_picker_selected(view: View):
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


# # Color Picker

# ## Basic
# Set `mode='color'` to show a color picker.
#
# The return value is a `(r, g, b, a)` tuple,
# where `r`, `g`, `b` are integers between 0-255,
# and `a` is an integer between 0-100%.
def color_basic(view: View):
    color = view(box('Choose a color', mode='color'))
    r, g, b, a = color
    view(f'You chose the color `rgba({r}, {g}, {b}, {a}%)`.')


# ## Value
# Set `value=` to pre-select a color.
#
# A color value can be:
#
# - `#RRGGBB` e.g. `#ff0033`
# - `#RRGGBBAA` e.g. `#ff003388`
# - `#RGB` e.g. `#f03` (same as `#ff0033`)
# - `#RGBA` e.g. `#f038` (same as `#ff003388`)
# - `rgb(R,G,B)` e.g. `rgb(255, 0, 127)` or `rgb(100%, 0%, 50%)`
# - `rgba(R,G,B,A)` e.g. `rgb(255, 0, 127, 0.5)` or `rgb(100%, 0%, 50%, 50%)`
# - `hsl(H,S,L)` e.g. `hsl(348, 100%, 50%)`
# - `hsl(H,S,L,A)` e.g. `hsl(348, 100%, 50%, 0.5)` or `hsl(348, 100%, 50%, 50%)`
# - A [named color](https://drafts.csswg.org/css-color-3/#svg-color) e.g. `red`, `green`, `blue`, etc.
# - `transparent` (same as `rgba(0,0,0,0)`)
#
# The return value, as in the previous example, is a `(r, g, b, a)` tuple.
def color_value(view: View):
    color = view(box('Choose a color', mode='color', value='#a241e8'))
    view(f'You chose {color}.')


# # Color Palette

# ## Basic
# Set `options=` with `mode='color'` to show a color palette.
#
# The option's `value` must be a valid color in one of the formats described in the previous example.
#
# Unlike the Color Picker, the Color Palette returns the `value` of the chosen option, and not a `(r,g,b,a)` tuple.
def palette_basic(view: View):
    color = view(box('Choose a color', mode='color', options=[
        option('#ff0000', 'Red'),
        option('#00ff00', 'Green'),
        option('#0000ff', 'Blue'),
        option('#ffff00', 'Yellow'),
        option('#00ffff', 'Cyan'),
        option('#ff00ff', 'Magenta'),
    ]))
    view(f'You chose {color}.')


# ## Value
# Set `value=` to pre-select an option having that color value.
def palette_value(view: View):
    color = view(box('Choose a color', mode='color', value='#0000ff', options=[
        option('#ff0000', 'Red'),
        option('#00ff00', 'Green'),
        option('#0000ff', 'Blue'),
        option('#ffff00', 'Yellow'),
        option('#00ffff', 'Cyan'),
        option('#ff00ff', 'Magenta'),
    ]))
    view(f'You chose {color}.')


# ## Selected
# Alternatively, set `selected=True` to pre-select a color in the palette.
def palette_selected(view: View):
    color = view(box('Choose a color', mode='color', options=[
        option('#ff0000', 'Red'),
        option('#00ff00', 'Green'),
        option('#0000ff', 'Blue', selected=True),
        option('#ffff00', 'Yellow'),
        option('#00ffff', 'Cyan'),
        option('#ff00ff', 'Magenta'),
    ]))
    view(f'You chose {color}.')


# # Rating

# ## Basic
# Set `mode='rating'` to accept a star-rating.
#
# By default, five stars are displayed.
def rating_basic(view: View):
    stars = view(box('Rate your experience', mode='rating'))
    view(f'Your rating was {stars} stars.')


# ## Value
# Set `value=` to specify a default value.
def rating_value(view: View):
    stars = view(box('Rate your experience', mode='rating', value=3))
    view(f'Your rating was {stars} stars.')


# ## Min
# Set `min=0` to allow zero stars.
def rating_min(view: View):
    stars = view(box('Rate your experience', mode='rating', min=0))
    view(f'Your rating was {stars} stars.')


# ## Max
# Set `max=` to increase the number of stars displayed.
def rating_max(view: View):
    stars = view(box('Rate your experience', mode='rating', value=3, max=10))
    view(f'Your rating was {stars} stars.')


# ## Min and max
# `min=` and `max=` can be combined.
def rating_min_max(view: View):
    stars = view(box('Rate your experience', mode='rating', value=3, min=0, max=10))
    view(f'Your rating was {stars} stars.')


# ## Range
# Set `range=` to a `(min, max)` tuple to control min/max stars.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def rating_range(view: View):
    stars = view(box('Rate your experience', mode='rating', value=3, range=(0, 10)))
    view(f'Your rating was {stars} stars.')


# # Theming

# ## Color Variables
# To use pre-defined, named colors that sit well with the app's theme, use *color variables*.
# Color variables take the form `var(--name)` or simply `$name`.
# For example, you can use `var(--red)` or `$red` instead of hard-coded colors like `red` or `#ff0000` or `rgb(255,0,0)`.
#
# Color variables can be passed wherever colors are accepted, like `background`, `border`, `color`, and so on.
#
# There are 16 pre-defined *spectrum colors*, derived automatically from the theme's accent color, by matching its
# saturation and lightness. The naming of each color is indicative, and its hue might appear off depending on the
# position of the accent color's hue along the color spectrum. For example, `$red` could appear pink or orange!
#
# Additionally, there are pre-defined color variables for various *tones* of the theme's foreground (`$foreground`),
# background (`$background`) and accent (`$accent`) colors.
# Accent color tones are prefixed with `$accent-`, and neutral tones (grays) are prefixed with `$neutral-`.
def theme_colors(view: View):
    style = dict(width='35px', height='35px', border='#777', margin='0 0 2.5rem 0')
    view(
        '### Spectrum Colors',
        row(
            box(background='$red', **style),
            box(background='$lava', **style),
            box(background='$orange', **style),
            box(background='$amber', **style),
            box(background='$yellow', **style),
            box(background='$lime', **style),
            box(background='$mint', **style),
            box(background='$green', **style),
            box(background='$teal', **style),
            box(background='$cyan', **style),
            box(background='$sky', **style),
            box(background='$blue', **style),
            box(background='$indigo', **style),
            box(background='$purple', **style),
            box(background='$violet', **style),
            box(background='$pink', **style),
            wrap='normal',
        ),
        '### Theme Colors',
        row(
            box(background='$foreground', **style),
            box(background='$background', **style),
            box(background='$accent', **style),
            wrap='normal',
        ),
        '### Accent Tones',
        row(
            box(background='$accent-darker', **style),
            box(background='$accent-dark', **style),
            box(background='$accent-dark-alt', **style),
            box(background='$accent-primary', **style),
            box(background='$accent-secondary', **style),
            box(background='$accent-tertiary', **style),
            box(background='$accent-light', **style),
            box(background='$accent-lighter', **style),
            box(background='$accent-lighter-alt', **style),
            wrap='normal',
        ),
        '### Neutral Tones',
        row(
            box(background='$neutral-dark', **style),
            box(background='$neutral-primary', **style),
            box(background='$neutral-primary-alt', **style),
            box(background='$neutral-secondary', **style),
            box(background='$neutral-secondary-alt', **style),
            box(background='$neutral-tertiary', **style),
            box(background='$neutral-tertiary-alt', **style),
            box(background='$neutral-quaternary', **style),
            box(background='$neutral-quaternary-alt', **style),
            box(background='$neutral-light', **style),
            box(background='$neutral-lighter', **style),
            box(background='$neutral-lighter-alt', **style),
            wrap='normal',
        ),
    )


# # Advanced Layout

# ## An Album
# A simple layout for photo galleries or portfolios.
#
# Inspired by the [Bootstrap Album](https://getbootstrap.com/docs/4.0/examples/album/).
def layout_album(view: View):
    cards = [make_album_card(lorem(1), i) for i in range(9)]

    view(
        col(
            box(f'## {lorem()}\n\n{lorem(3)}', align='center'),
            box(dict(yes='Primary', no='Secondary'), align='center'),
            color='$background', background='$foreground',
            padding='8rem', tile='center',
        ),
        row(
            *cards,
            background='$neutral-lighter',
            wrap='between', tile='center', padding='3rem'
        ),
        gap=0,
    )


def make_album_card(text, views):
    return col(
        box('Thumbnail', tile='center', cross_tile='center', height=200, background='$neutral-tertiary'),
        box(text, padding='0 1rem'),
        row(
            box(mode='button', options=[
                option('view', 'View', selected=False, options=[
                    option('edit', 'Edit', icon='Edit')
                ])
            ]),
            box(f'{views + 1} views', align='right', color='$neutral-secondary'),
            padding='1rem', tile='between', cross_tile='end',
        ),
        background='$background', border='$neutral-tertiary-alt',
        padding=0, width='32%',
    )
