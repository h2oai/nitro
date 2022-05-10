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


# # Popups

# ## Basic
# Call `view()` with `popup=True` to show the view on a popup window.
def popup_basic(view: View):
    view(box(['Show a popup']))
    view('Wait! Call us now for free donuts!', popup=True)


# ## Set popup title
# Set `title=` to set a title for the popup window.
def popup_title(view: View):
    view(box(['Show a popup']))
    view('Call us now for free donuts!', title='Wait!', popup=True)


# ## Customize buttons
# If the popup's body contains a set of buttons, they're used as the popup's dismiss buttons. Common uses for such
# buttons are to accept, cancel or close a popup.
def popup_buttons(view: View):
    view(box(['Show a popup']))
    response = view(
        box('Call us now for free donuts!'),
        box(dict(yes='Yes, now!', no='Maybe later')),
        title='Wait!', popup=True,
    )
    if response == 'yes':
        view('Your donuts are on the way!')
    else:
        view('No donuts for you.')
