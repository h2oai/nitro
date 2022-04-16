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
