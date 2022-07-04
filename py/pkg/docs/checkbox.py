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


# # Checkbox
# Use a checkbox to choose between two mutually exclusive options.

# ## Basic
# Set `mode='check'` to show a checkbox.
def checkbox_basic(view: View):  # height 2
    keep_signed_in = view(box('Keep me signed in', mode='check'))
    view(f'Keep me signed in: {keep_signed_in}.')


# ## Set initial value
# Set `value=True` to pre-select the checkbox.
#
# The mode setting `mode='check'` is implied, and can be elided.
def checkbox_value(view: View):  # height 2
    keep_signed_in = view(box('Keep me signed in', value=True))
    view(f'Keep me signed in: {keep_signed_in}.')


# ## Handle changes immediately
# Set `live=True` to handle changes immediately.
def checkbox_live(view: View):  # height 2
    keep_signed_in = True
    while True:
        keep_signed_in = view(
            box('Remember me', value=keep_signed_in, live=True),
            "Keep me signed in." if keep_signed_in else "Don't keep me signed in.",
        )
