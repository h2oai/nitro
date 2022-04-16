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
