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


# # Textbox
# Use textboxes to capture text inputs and passwords.

# ## Basic
# Call `box()` with `mode='text'` to show a textbox.
#
# The return value is the text entered into the box.
def textbox_basic(view: View):  # height 2
    x = view(box(mode='text'))
    view(f'You entered {x}.')


# ## Set initial value
# Set `value=` to prefill the box with a value.
#
# `mode='text'` can be elided if `value=` is set.
def textbox_value(view: View):  # height 2
    speed = view(box(value='60 km/h'))
    view(f'Your speed is {speed}.')


# ## Set a label
# Any text passed to `box()` is used as a label.
def textbox_label(view: View):  # height 2
    speed = view(box('Speed', value='60'))
    view(f'Your speed is {speed} km/h.')


# ## Show placeholder text
# Use `placeholder=` to show placeholder text inside the box.
def textbox_placeholder(view: View):  # height 2
    speed = view(box('Speed', placeholder='0 km/h'))
    view(f'Your speed is {speed} km/h.')


# ## Mark as required
# Add `required` to `mode` to indicate that input is required.
def textbox_required(view: View):  # height 2
    speed = view(box('Speed (km/h)', mode='required'))
    view(f'Your speed is {speed} km/h.')


# ## Control input format
# Set `mask=` to specify an input mask. An input mask is used to format the text field
# for the expected entry.
#
# For example, to accept a phone number, use an input mask containing three sets of digits.
def textbox_mask(view: View):  # height 2
    phone = view(box('Phone', mask='(999) 999 - 9999'))
    view(f'Your phone number is {phone}.')


# To construct the input mask:
#
# - Use `a` to indicate a letter.
# - Use `9` to indicate a number.
# - Use `*` to indicate a letter or number.
# - Use a backslash to escape any character.

# ## Show an icon
# Set `icon=` to show an icon at the end of the box.
def textbox_icon(view: View):  # height 2
    phrase = view(box('Filter results containing:', icon='Filter'))
    view(f'You set a filter on `{phrase}`.')


# ## Set prefix text
# Set `prefix=` to show a prefix at the start of the box.
def textbox_prefix(view: View):  # height 2
    website = view(box('Website', prefix='https://', value='example.com'))
    view(f'Your website is https://{website}.')


# ## Set suffix text
# Set `suffix=` to show a suffix at the end of the box.
def textbox_suffix(view: View):  # height 2
    website = view(box('Website', suffix='.com', value='example'))
    view(f'Your website is {website}.com.')


# ## Set both prefix and suffix texts
# A textbox can show both a prefix and a suffix at the same time.
def textbox_prefix_suffix(view: View):  # height 2
    website = view(box('Website', prefix='https://', suffix='.com', value='example'))
    view(f'Your website is https://{website}.com.')


# ## Show an error message
# Set `error=` to show an error message below the box.
def textbox_error(view: View):  # height 2
    speed = view(box('Speed (km/h)', error='Invalid input'))


# ## Accept a password
# Add `password` to `mode` when accepting passwords and other confidential inputs.
def textbox_password(view: View):  # height 2
    password = view(box('Password field', mode='password'))
    view(f'Your password `{password}` is not strong enough!')


# ## Enable multiple lines
# Set `lines=` to show a multi-line text box (also called a *text area*).
def textarea(view: View):  # height 3
    bio = view(box('Bio:', lines=5))
    view(f'**Bio:** {bio}')


# Note that multi-line textboxes can be resized by the user,
# and `lines=` only sets the initial height of the textbox.

# ## Disable
# Set `disabled=True` to disable.
def textbox_disabled(view: View):  # height 2
    view(box(mode='text', disabled=True))
