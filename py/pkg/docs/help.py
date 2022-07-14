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


# # Help
# Show context-sensitive hints and help.

# ## Basic
# Set `help=` to associate context-sensitive help with a box.
#
# A _hint_ (or info) icon is displayed next to the box.
# Clicking on the icon displays the help content on a sidebar.
def help_basic(view: View):  # height 2
    choice = view(box(
        'Choose a flavor',
        mode='menu',
        options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
        help='All our flavors are 100% natural - no added sugar or colors!',
    ))
    view(f'You chose {choice}.')


# ## Using Markdown
# `help=` supports Markdown.
def help_markdown(view: View):  # height 2
    choice = view(box(
        'Choose a flavor',
        mode='menu',
        options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
        help='''
        ### No health risks!

        All our flavors are **100% natural** - no added sugar or colors!
        ''',
    ))
    view(f'You chose {choice}.')


# ## Localization
# Prefix the help with a `@` to show a locale-specific string.
#
# For example `help='@flavor_help` shows a locale-specific string named `flavor_help`, if available.
def help_localization(view: View):  # height 4
    choice = view(box(
        '@flavor_caption',
        mode='menu',
        options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
        help='@flavor_help',
    ))
    view(f'You chose {choice}.')


# ## Hint
# Set `hint=` to show an in-place pop-up hint when clicked.
#
# Hints are a lightweight alternative to showing long-form help.
# Use `hint=` instead of `help=` when you have 1-2 lines of text to display.
def hint_basic(view: View):  # height 2
    choice = view(box(
        'Choose a flavor',
        mode='menu',
        options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
        hint='All our flavors are 100% natural - no added sugar or colors!',
    ))
    view(f'You chose {choice}.')


# ## Hint with title
# If the hint contains multiple lines of text, the first line is used as the title.
def hint_title(view: View):  # height 2
    choice = view(box(
        'Choose a flavor',
        mode='menu',
        options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
        hint='No health risks!\nAll our flavors are 100% natural - no added sugar or colors!',
    ))
    view(f'You chose {choice}.')


# ## Hint localization
# Prefix the hint with a `@` to show a locale-specific string as the hint.
#
# For example `hint='@flavor_hint'` shows a locale-specific string named `flavor_hint`, if available.
def hint_localization(view: View):  # height 4
    choice = view(box(
        '@flavor_caption',
        mode='menu',
        options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
        hint='@flavor_hint',
    ))
    view(f'You chose {choice}.')
