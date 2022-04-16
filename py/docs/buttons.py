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
