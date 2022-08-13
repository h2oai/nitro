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


# # Styling
# Change how boxes look: colors, borders, sizing, margins, and padding.

# ## Basic
# Set `style=` to control how a box looks. Nitro supports [Tailwind](https://tailwindcss.com/) styles.
def styling_basic(view: View):  # height 2
    view(
        box(
            'Hello world!',
            # p-4: Padding, 4 units wide.
            # border-l-4: Border on the left, 4 pixels thick.
            # text-sm: Small text
            # font-medium: Medium font
            # text-sky-700: Dark blue text
            # bg-sky-50: Light blue background
            # border-sky-700: Dark blue border
            style='p-4 border-l-4 text-sm font-medium text-sky-700 bg-sky-50 border-sky-700',
        ),
    )


# ## Parts
# A part is a custom box with a preset style. Use `box.part()` to define a part.
#
# Parts can be used wherever `box(text, style='...')` feels repetitive.
def styling_part(view: View):  # height 3
    alert = box.part('p-4 border-l-4 text-sm font-medium text-sky-700 bg-sky-50 border-sky-700')

    view(
        alert('Begin at the beginning.'),
        alert('And go on till you come to the end.'),
        alert('Then stop.'),
    )


# ## Derived parts
# `box.part()` can extend existing parts.
#
# The example below creates different kinds of alerts from a base alert.
def styling_derived(view: View):  # height 3
    alert = box.part('p-4 border-l-4 text-sm font-medium')
    info_alert = box.part(alert, 'text-sky-700 bg-sky-50 border-sky-700')
    warning_alert = box.part(alert, 'text-amber-700 bg-amber-50 border-amber-700')
    critical_alert = box.part(alert, 'text-red-700 bg-red-50 border-red-700')

    view(
        info_alert('Begin at the beginning.'),
        warning_alert('And go on till you come to the end.'),
        critical_alert('Then stop.'),
    )


# ## Alert example
# The following example starts with a plain box and incrementally applies styles to create an alert box.
def styling_alert(view: View):  # height 2
    text = "I'm sorry, Dave. I can't do that."
    view(box(text), ['Increase font weight'])
    view(box(text, style='font-medium'), ['Make text smaller'])
    view(box(text, style='font-medium text-sm'), ['Change text color'])
    view(box(text, style='font-medium text-sm text-red-700'), ['Change background color'])
    view(box(text, style='font-medium text-sm text-red-700 bg-red-50'), ['Add padding'])
    view(box(text, style='font-medium text-sm text-red-700 bg-red-50 p-4'), ['Add border'])
    view(box(text, style='font-medium text-sm text-red-700 bg-red-50 p-4 border-l-4'), ['Change border color'])
    view(box(text, style='font-medium text-sm text-red-700 bg-red-50 p-4 border-l-4 border-red-700'), ['Restart'])


# ## Card example
# The following example starts with some nested and incrementally applies styles to create a card.
def styling_card(view: View):  # height 7
    title = 'Space Travel'
    text = lorem(2)
    image = box(image='sample.jpg')
    view(box(image, col(title, text)), ['Resize Card'])
    view(box(image, col(title, text), style='w-72'), ['Round corners'])
    view(box(image, col(title, text), style='w-72 rounded-xl'), ['Crop contents'])
    view(box(image, col(title, text), style='w-72 rounded-xl overflow-hidden'), ['Add shadow'])
    view(box(image, col(title, text), style='w-72 rounded-xl overflow-hidden shadow-xl'), ['Add padding'])
    view(box(image, col(title, text, style='p-4'), style='w-72 rounded-xl overflow-hidden shadow-xl'), ['Make title bold'])
    view(box(image, col(box(title, style='font-bold'), text, style='p-4'), style='w-72 rounded-xl overflow-hidden shadow-xl'), ['Make title larger'])
    view(box(image, col(box(title, style='font-bold text-xl'), text, style='p-4'), style='w-72 rounded-xl overflow-hidden shadow-xl'), ['Make text smaller'])
    view(box(image, col(box(title, style='font-bold text-xl'), box(text, style='text-sm'), style='p-4'), style='w-72 rounded-xl overflow-hidden shadow-xl'), ['Restart'])
