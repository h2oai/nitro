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

import datetime
from h2o_nitro import View, box, row, col, option, lorem


# # Format
# Learn the basics of formatting and templates.

# ## Basic
# Combine _templates_ with `data=` to perform string interpolation.
#
# A _template_ is any string that begins with a literal equals `=` symbol.
#
# Nitro's templates are more powerful than Python's formatted string literals (f-strings) in at least two ways:
#
# - Nitro's formatting is _locale-sensitive_. For example, if a number `123456.789` was used in a template, users in
#   the United States would see `123,456.789`, Germany would see `123,456.789`, and India would see `1,23,456.789`.
# - You can pass _styles_ to control how each element is displayed, much like a box's visual style.
#   For example, the number `total` below uses the `cur-USD` currency style, which shows the number in US Dollars,
#   and `quota` uses the `pct` style, which shows the percentage.
def format_basic(view: View):  # height 2
    view(
        box(
            '=You bought {count} {product}.',
            data=dict(count=42, product='donuts'),
        ),
        box(
            '=Your total is {total cur-USD} ({quota pct} of your allowance).',
            data=dict(total=84.99, quota=0.4178978625),
        ),
    )


# ## Nested data
# Use dot-notation to access nested data.
def format_nested(view: View):  # height 2
    view(box(
        '={greeting}, {name.first} {name.last}!',
        data=dict(
            greeting='Hello',
            name=dict(
                first='Boaty',
                last='McBoatface',
            ),
        )
    ))


# ## Arrays
# Use 0-based integers to access arrays.
#
# This notation is more compact, but less readable.
def format_array(view: View):  # height 2
    view(box('={0}, {1} {2}!', data=['Hello', 'Boaty', 'McBoatface']))


# ## Nested arrays
# Combine dot-notation with 0-based integers to access nested arrays.
def format_nested_array(view: View):  # height 2
    view(box(
        '={greeting}, {name.0} {name.1}!',
        data=dict(greeting='Hello', name=['Boaty', 'McBoatface'])
    ))


# ## Format number
# Set the `num`, `pct`, `sci`, `eng`, `cur`, or `unit` styles to format numbers.
#
# - `num`: decimal
# - `pct`: percent
# - `sci`: scientific notation
# - `eng`: engineering notation
# - `cur`: currency
# - `unit`: units
#
# Advanced options are covered in a later section on number formatting.
def format_number(view: View):
    view(
        # Format using active application-wide locale.
        box('=Decimal: {donuts num}', data=dict(donuts=123456.789)),

        # The 'num' style is implied since 'donuts' is a number.
        box('=Default: {donuts}', data=dict(donuts=123456.789)),

        # Percent
        box('=Percent: {donuts pct}', data=dict(donuts=123456.789)),

        # Scientific notation
        box('=Scientific: {donuts sci}', data=dict(donuts=123456.789)),

        # Engineering notation
        box('=Engineering: {donuts eng}', data=dict(donuts=123456.789)),

        # Currency
        box('=Currency: {donuts cur-USD}', data=dict(donuts=123456.789)),

        # Units
        box('=Units: {donuts unit-ounce}', data=dict(donuts=123456.789)),
    )


# ## Format date
# Set the `date`, `time`, or `datetime` styles to format dates.
#
# Advanced options are covered in a later section on date and time formatting.
def format_date(view: View):  # height 3
    # Launch 100 days from now.
    launch_date = (datetime.datetime.now() + datetime.timedelta(days=100)).isoformat()
    view(
        box('=Launch date: {launch date}.', data=dict(launch=launch_date)),
        box('=Launch time: {launch time}.', data=dict(launch=launch_date)),
        box('=Launch date and time: {launch date time}.', data=dict(launch=launch_date)),
    )


# ## Format lists
# Set the `and`, `or`, or `list` styles to format lists.
def format_list(view: View):  # height 6
    view(
        '## English',

        # Locale-sensitive list
        box('=Colors: {colors list}', data=dict(colors=['red', 'green', 'blue'])),

        # The 'list' style is implied since 'color' is a list.
        box('=Colors: {colors}', data=dict(colors=['red', 'green', 'blue'])),

        # Locale-sensitive conjunction
        box('=Colors: {colors and}', data=dict(colors=['red', 'green', 'blue'])),

        # Locale-sensitive disjunction
        box('=Colors: {colors or}', data=dict(colors=['red', 'green', 'blue'])),

        '## German',
        box('=Colors: {colors list}', data=dict(colors=['red', 'green', 'blue']), locale='de'),
        box('=Colors: {colors}', data=dict(colors=['red', 'green', 'blue']), locale='de'),
        box('=Colors: {colors and}', data=dict(colors=['red', 'green', 'blue']), locale='de'),
        box('=Colors: {colors or}', data=dict(colors=['red', 'green', 'blue']), locale='de'),

    )


# ## Format list sizes
# Suffix the `and`, `or`, or `list` styles with `-l` (long), `-s` (short), or `-xs` (extra-short)
# to fine-tune formatting.
def format_list_sizes(view: View):  # height 6
    view(
        '## List',
        box('=Colors: {colors list-l}', data=dict(colors=['red', 'green', 'blue'])),
        box('=Colors: {colors list-s}', data=dict(colors=['red', 'green', 'blue'])),
        box('=Colors: {colors list-xs}', data=dict(colors=['red', 'green', 'blue'])),
        '## And',
        box('=Colors: {colors and-l}', data=dict(colors=['red', 'green', 'blue'])),
        box('=Colors: {colors and-s}', data=dict(colors=['red', 'green', 'blue'])),
        box('=Colors: {colors and-xs}', data=dict(colors=['red', 'green', 'blue'])),
        '## Or',
        box('=Colors: {colors or-l}', data=dict(colors=['red', 'green', 'blue'])),
        box('=Colors: {colors or-s}', data=dict(colors=['red', 'green', 'blue'])),
        box('=Colors: {colors or-xs}', data=dict(colors=['red', 'green', 'blue'])),
    )
