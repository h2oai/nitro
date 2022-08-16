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
# Learn the basics of collecting inputs from the user.

# ## Basic
# To create a form, simply lay out all the inputs you need inside a view, then destructure the return value in order.
def form_basic(view: View):  # height 3
    username, password, action = view(
        box('Username', value='someone@company.com'),
        box('Password', mode='password', value='pa55w0rd'),
        box(['Login']),
    )
    view(f'You entered `{username}`/`{password}` and then clicked on {action}.')


# ## Horizontal
# Wrap items with `row()` to lay them out left to right.
# There is no change to the way the return values are destructured.
def form_horizontal(view: View):  # height 2
    username, password, action = view(
        row(
            box('Username', value='someone@company.com'),
            box('Password', mode='password', value='pa55w0rd'),
            box(['Login']),
        )
    )
    view(f'You entered `{username}`/`{password}` and then clicked on {action}.')


# ## Combined
# Use `row()` and `col()` to mix and match how items are laid out. Destructure the return values in the same order.
def form_combo(view: View):  # height 4
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
# Specify additional styles like `w-*`, `grow`, etc. to get more control over how items are laid out.
def form_improved(view: View):  # height 5
    first, middle, last, addr1, addr2, city, state, zip, action = view(
        row(
            box('First name', value=''),
            box('M.I.', value='') / 'w-1/10',  # shrink
            box('Last name', value=''),
        ),
        box('Address line 1', value=''),
        box('Address line 2', value=''),
        row(
            box('City', value='') / 'grow',  # grow
            box('State', value='') / 'w-1/5',  # shrink
            box('Zip', value='') / 'grow',  # grow
        ),
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


# ## Tabs
# Groups together related boxes inside `row()` to display a tabbed layout.
def form_tabs(view: View):  # height 4
    view(
        row(
            box(
                box('First name', value='Boaty'),
                box('Last name', value='McBoatface'),
                box('Age', value=42),
                title='Profile',
            ),
            box(
                box('Billing address line 1', value=''),
                box('Billing address line 2', value=''),
                row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                title='Billing Address',
            ),
            box(
                box('Shipping address line 1', value=''),
                box('Shipping address line 2', value=''),
                row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                title='Shipping Address',
            ),
        )
    )


# ## Vertical tabs
# Groups together related boxes inside `col()` to display a vertical tabbed layout.
def form_tabs_vertical(view: View):  # height 3
    view(
        col(
            box(
                box('First name', value='Boaty'),
                box('Last name', value='McBoatface'),
                box('Age', value=42),
                title='Profile',
                icon='Contact',
            ),
            box(
                box('Billing address line 1', value=''),
                box('Billing address line 2', value=''),
                row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                title='Billing Address',
                icon='PaymentCard',
            ),
            box(
                box('Shipping address line 1', value=''),
                box('Shipping address line 2', value=''),
                row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                title='Shipping Address',
                icon='DeliveryTruck',
            ),
        )
    )
