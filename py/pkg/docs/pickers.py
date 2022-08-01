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


# # Pickers
# Use pickers to pick one or more options from several options.
# Buttons, checklists, dropdowns, and color pickers are all examples of pickers.

# ## Basic
# A *picker* is a box that allows the user to pick one or more options from a group.
# Buttons, checklists, dropdowns, and color pickers are all examples of pickers.
#
# Set `options=` to create a picker.
def picker_basic(view: View):  # height 3
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


# ## Show buttons
# Buttons are shown for up to 3 options.
#
# Set `mode='button'` to display buttons regardless of the number of options.
def picker_buttons(view: View):  # height 1
    choice = view(box('Choose a color', options=[
        'yellow', 'orange', 'red'
    ]))
    view(f'You chose {choice}.')


# ## Show radio buttons
# Radio buttons are shown for 4-7 options.
#
# Set `mode='radio'` to display radio buttons regardless of the number of options.
def picker_radio(view: View):  # height 3
    choice = view(box('Choose a color', options=[
        'green', 'yellow', 'orange', 'red'
    ]))
    view(f'You chose {choice}.')


# ## Show a dropdown menu
# A dropdown menu is shown for more than 7 options.
#
# Set `mode='menu'` to display a dropdown menu regardless of the number of options.
def picker_dropdown(view: View):  # height 2
    choice = view(box('Choose a color', options=[
        'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Show a dropdown list
# Add `multi` to `mode` to allow choosing more than one option. The return value is a list of choices made.
#
# By default, this displays checkboxes for up to 7 options, or a dropdown menu for more than 7 options.
#
# Set `mode='menu'` to display a dropdown menu regardless of the number of options.
def picker_multiple_dropdown(view: View):  # height 2
    choices = view(box('Choose some colors', mode='multi', options=[
        'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choices}.')


# ## Show a checklist
# A checklist is shown for up to 7 options when `multi` is set.
#
# Set `mode='check'` to display a checklist regardless of the number of options.
def picker_checklist(view: View):  # height 3
    choices = view(box('Choose some colors', mode='multi check', options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choices}.')


# ## Mark as required
# Add `required` to `mode` to indicate that input is required.
def picker_dropdown_required(view: View):  # height 2
    choice = view(box('Choose a color', mode='required menu', options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')


# ## Show an error message
# Set `error=` to show an error message below the box.
def picker_dropdown_error(view: View):  # height 2
    choice = view(box('Choose a color', mode='menu', error='Invalid input', options=[
        'yellow', 'orange', 'red', 'black'
    ]))
    view(f'You chose {choice}.')
