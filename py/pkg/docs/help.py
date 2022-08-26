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
def help_basic(view: View):  # height 3
    choice = view(box(
        'Choose a flavor',
        mode='menu',
        options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
        help='All our flavors are 100% natural - no added sugar or colors!',
    ))
    view(f'You chose {choice}.')


# ## Using Markdown
# `help=` supports Markdown.
def help_markdown(view: View):  # height 3
    choice = view(box(
        'Choose a flavor',
        mode='menu',
        options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
        help='''
        ### No health risks!

        All our flavors are **100% natural** - no added sugar or colors!
        
        [Learn more](https://www.example.com)
        ''',
    ))
    view(f'You chose {choice}.')


# ## Localization
# Prefix the help with a `@` to show a locale-specific string.
#
# For example `help='@flavor_help` shows a locale-specific string named `flavor_help`, if available.
def help_localization(view: View):  # height 3
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


# ## Hint with help
# If a box has both `hint=` and `help=` set, the hint will automatically show a button that launches help.
def hint_help(view: View):  # height 2
    choice = view(box(
        'Choose a flavor',
        mode='menu',
        options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
        hint='No health risks!\nAll our flavors are 100% natural - no added sugar or colors!',
        help='''
        ### What goes into our flavoring?
        
        Our flavors contain the essential oil, oleoresin, essence or extractive, protein hydrolysate, distillate, 
        or any product of roasting, heating or enzymolysis, which contains the flavoring constituents derived from 
        a spice, fruit or fruit juice, vegetable or vegetable juice, edible yeast, herb, bark, bud, root, leaf or 
        similar plant material, meat, seafood, poultry, eggs, dairy products, or fermentation products thereof, 
        whose significant function in food is flavoring rather than nutritional.
        ''',
    ))
    view(f'You chose {choice}.')


# ## Hint localization
# Prefix the hint with a `@` to show a locale-specific string as the hint.
#
# For example `hint='@flavor_hint'` shows a locale-specific string named `flavor_hint`, if available.
def hint_localization(view: View):  # height 2
    choice = view(box(
        '@flavor_caption',
        mode='menu',
        options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
        hint='@flavor_hint',
    ))
    view(f'You chose {choice}.')


# ## More examples
# Almost all boxes in Nitro support `hint=` and `help=`.
def help_examples(view: View):  # height 10
    hint = 'Here is a hint about this box!'
    flavors = ['Vanilla', 'Strawberry', 'Blueberry']
    view(
        box('Your name', value='Jelly McJellyface', hint=hint),
        box('How many donuts?', mode='number', hint=hint),
        box('Add sprinkles', mode='check', hint=hint),
        box('Add sprinkles', mode='toggle', value=True, hint=hint),
        box('Choose a flavor', mode='button', options=flavors, hint=hint),
        box('Choose a flavor', mode='menu', options=flavors, hint=hint),
        box('Choose a flavor', mode='multi menu', options=flavors,  hint=hint),
        box('Choose a flavor', mode='radio', options=flavors, hint=hint),
        box('Choose a flavor', mode='check', options=flavors, hint=hint),
        box('How many donuts?', mode='range', value=5, hint=hint),
        box('Party size', mode='range', value=(3, 7), hint=hint),
        box('Pick a time', mode='time', value='3:04PM', hint=hint),
        box('Pick a date', mode='date', hint=hint),
        box('Pick a week', mode='week', hint=hint),
        box('Pick a month', mode='month', hint=hint),
        box('Pick a date', mode='day', hint=hint),
        box('Choose a flavor', mode='tag', options=flavors, hint=hint),
        box('Package color', mode='color', options=[
            option('#ff0000', 'Red'),
            option('#00ff00', 'Green'),
            option('#0000ff', 'Blue'),
        ], hint=hint),
        box('Package color', mode='color', hint=hint),
        box('Rate your experience', mode='rating', hint=hint),
    )
