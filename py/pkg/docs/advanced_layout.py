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


# # Advanced
# Learn some advanced tips and tricks to level up your Nitro skills.

# ## Embed web pages in a view
# Set `mode='web'` to embed external web pages.
def embed_iframe(view: View):  # height 5
    view(box(mode='web', path='https://example.com', style='h-96'))


# ## Open web pages in a new view
# Pass a URL to `view.jump()` with `target='_blank'` to open web pages in a new view.
def open_web_page_blank(view: View):  # height 2
    view('Click Continue to open https://example.com in a new view.')
    view.jump('https://example.com')


# ## Open web pages in a popup
# URLs can be opened in popup windows by passing `popup=1`.
def open_web_page_popup(view: View):  # height 2
    view('Click Continue to open https://example.com in a new view.')
    view.jump('https://example.com', popup=1, width=400, height=300, left=100, top=100)


# ## Open web pages in the current view
# Pass a URL to `view.jump()` to open web pages in the current view.
def open_web_page(view: View):  # height 2
    view('Click Continue to open https://example.com in the current view.')
    view.jump('https://example.com', target='_self')


# ## Open web pages in the top level view
# Pass a URL to `view.jump()` with `target='_top'` to open web pages in the top level view.
def open_web_page_top(view: View):  # height 2
    view('Click Continue to open https://example.com in the top level view.')
    view.jump('https://example.com', target='_top')
