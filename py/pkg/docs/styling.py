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

# ## Tag
def styling_tag(view: View):
    view(
        row(
            box('Info',
                style='border text-sky-500 border-current uppercase px-5 py-1.5 rounded-full text-xs tracking-wide'),
            box('Info',
                style='border text-white border-sky-500 bg-sky-500 uppercase px-5 py-1.5 rounded-full text-xs tracking-wide'),
            box('Info',
                style='border text-sky-500 border-sky-500 bg-sky-100 uppercase px-5 py-1.5 rounded-full text-xs tracking-wide'),
        ),
        row(
            box('Warning',
                style='border text-amber-500 border-current uppercase px-5 py-1.5 rounded-full text-xs tracking-wide'),
            box('Warning',
                style='border text-white border-amber-500 bg-amber-500 uppercase px-5 py-1.5 rounded-full text-xs tracking-wide'),
            box('Warning',
                style='border text-amber-500 border-amber-500 bg-amber-100 uppercase px-5 py-1.5 rounded-full text-xs tracking-wide'),
        ),
        row(
            box('Success',
                style='border text-green-500 border-current uppercase px-5 py-1.5 rounded-full text-xs tracking-wide'),
            box('Success',
                style='border text-white border-green-500 bg-green-500 uppercase px-5 py-1.5 rounded-full text-xs tracking-wide'),
            box('Success',
                style='border text-green-500 border-green-500 bg-green-100 uppercase px-5 py-1.5 rounded-full text-xs tracking-wide'),
        ),
        row(
            box('Critical',
                style='border text-red-500 border-current uppercase px-5 py-1.5 rounded-full text-xs tracking-wide'),
            box('Critical',
                style='border text-white border-red-500 bg-red-500 uppercase px-5 py-1.5 rounded-full text-xs tracking-wide'),
            box('Critical',
                style='border text-red-500 border-red-500 bg-red-100 uppercase px-5 py-1.5 rounded-full text-xs tracking-wide'),
        ),
    )


# ## Persona
def styling_persona(view: View):
    view(
        row(
            box(image='sample.jpg', style='object-cover w-6 h-6 rounded-full'),
            box('Boaty McBoatface', style='text-xs font-medium'),
            style='items-center bg-gray-100 pl-2 pr-3 py-1.5 rounded-full',
        ),
        row(
            box('Boaty McBoatface', style='text-xs font-medium'),
            box(image='sample.jpg', style='object-cover w-6 h-6 rounded-full'),
            style='items-center bg-gray-100 pr-2 pl-3 py-1.5 rounded-full',
        ),
    )


# ## Badge
def styling_badges(view: View):
    view(
        row(
            row(
                box('Status: ', style='text-gray-700'),
                box('System available', style='text-sky-700'),
                style='items-center border border-gray-200 rounded text-xs font-medium px-2.5 py-1.5',
            ),
            row(
                box('Status: ', style='text-gray-700'),
                box('System paused', style='text-amber-700'),
                style='items-center border border-gray-200 rounded text-xs font-medium px-2.5 py-1.5',
            ),
            row(
                box('Status: ', style='text-gray-700'),
                box('System normal', style='text-green-700'),
                style='items-center border border-gray-200 rounded text-xs font-medium px-2.5 py-1.5',
            ),
            row(
                box('Status: ', style='text-gray-700'),
                box('System overload', style='text-red-700'),
                style='items-center border border-gray-200 rounded text-xs font-medium px-2.5 py-1.5',
            )
        )
    )


# ## CTA
def style_cta_light(view: View):
    view(
        col(
            box('Handcrafted Espresso Drinks', mode='box'),
            box('Sipping is believing', style='text-indigo-700'),
            style='text-5xl font-extrabold tracking-tight',
        ),
        box(lorem(5), style='mt-4'),
        box(['Get Started', 'Learn More'], style='justify-center'),
        style='bg-gray-50 px-4 py-32 text-center',

    )


# ## Dark CTA
def style_cta_dark(view: View):
    view(
        col(
            box('Handcrafted Espresso Drinks', mode='box'),
            box('Sipping is believing', mode='box'),
            style='text-5xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-green-300 via-blue-500 to-purple-600',
        ),
        box(lorem(5), style='mt-4'),
        box(['Get Started', 'Learn More'], style='justify-center'),
        style='text-white bg-gray-900 px-4 py-32 text-center',
    )


# ## Alert
def styling_alert(view: View):
    view(
        col(
            box('Your system is up to date.', style='text-sm font-medium'),
            box(lorem(5), style='text-xs'),
            style='p-4 text-sky-700 border rounded border-sky-200 bg-sky-50',
        ),
        col(
            box('A system update is available.', style='text-sm font-medium'),
            box(lorem(5), style='text-xs'),
            style='p-4 text-amber-700 border rounded border-amber-200 bg-amber-50',
        ),
        col(
            box('System update successful!', style='text-sm font-medium'),
            box(lorem(5), style='text-xs'),
            style='p-4 text-green-700 border rounded border-green-200 bg-green-50',
        ),
        col(
            box('System update failed.', style='text-sm font-medium'),
            box(lorem(5), style='text-xs'),
            style='p-4 text-red-700 border rounded border-red-200 bg-red-50',
        ),
    )


# ## Alert strip
def styling_alert_strip(view: View):
    view(
        box('Your system is up to date.',
            style='p-4 text-sky-700 border-l-4 border-sky-700 bg-sky-50 text-sm font-medium'),
        box('A system update is available.',
            style='p-4 text-amber-700 border-l-4 border-amber-700 bg-amber-50 text-sm font-medium'),
        box('System update successful!',
            style='p-4 text-green-700 border-l-4 border-green-700 bg-green-50 text-sm font-medium'),
        box('System update failed.',
            style='p-4 text-red-700 border-l-4 border-red-700 bg-red-50 text-sm font-medium'),
    )

    text = lorem(3)
    view(
    )
