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


# # Cards
# Create content cards by stacking boxes together.

# ## Basic
def card_basic(view: View):  # height 4
    icon = '''
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
    </svg>
    '''
    view(
        box(
            box('4.2',
                style='absolute top-4 right-4 rounded-full px-3 py-1.5 bg-green-100 text-green-600 font-medium text-xs'),
            col(
                box(icon, mode='svg', style='w-10 h-10'),
                box(lorem(), style='text-xl font-bold text-gray-900'),
                box(lorem(2), style='text-sm'),
                style='text-gray-500 pr-8',
            ),
            style='relative p-8 border shadow hover:shadow-xl rounded-xl',
        ),
        style='w-96',
    )


# ## With gradient border
def card_gradient_border(view: View):  # height 4
    view(
        box(
            box(
                box(
                    box('To space and beyond', style='text-xl font-bold text-gray-900'),
                    box(lorem(2), style='mt-2 text-sm text-gray-500'),
                    style='mt-16 pr-8',
                ),
                style='absolute inset-1 bg-white p-8 rounded-xl'
            ),
            style='relative h-72 shadow-xl bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500 rounded-2xl',
        ),
        style='w-96',
    )


# ## With image
def card_image(view: View):
    view(
        box(
            box(image='sample.jpg', style='object-cover w-full h-56'),
            box(
                box('To space and beyond', style='text-xl font-bold'),
                box(lorem(2), style='mt-2 text-sm text-gray-500'),
                box('Find out more →',
                    style='inline-block pb-1 mt-4 font-medium text-indigo-600 border-b border-indigo-500'),
                style='p-6',
            ),
            style='overflow-hidden border border-gray-100 rounded-lg shadow-sm',
        ),
        style='w-96',
    )


# ## Dark with image
def card_dark_image(view: View):
    view(
        box(
            box(image='sample.jpg', style='object-cover w-full h-56'),
            box(
                box('Rocketry', style='text-xs text-gray-400'),
                box('To space and beyond', style='text-sm text-white'),
                box(lorem(2), style='mt-1 text-xs text-gray-300'),
                style='p-4 bg-gray-900',
            ),
            style='overflow-hidden rounded-2xl',
        ),
        style='w-96',
    )


# ## With stats
def card_stats(view: View):
    view(
        box(
            row(
                box(
                    box('To space and beyond', style='text-xl font-bold text-gray-900'),
                    box('By Boaty McBoatface', style='mt-1 text-xs font-medium text-gray-600')
                ),
                box(
                    box(image='sample.jpg', style='object-cover w-16 h-16 rounded-lg shadow-sm'),
                    style='flex-shrink-0 ml-3',
                ),
                style='justify-between',
            ),
            box(lorem(4), style='mt-4 pr-12 text-sm text-gray-500'),
            row(
                box(
                    box('2nd Apr 2024', style='text-xs text-gray-500'),
                    box('Published', style='text-sm font-medium text-gray-600'),
                ),
                box(
                    box('42 minutes', style='text-xs text-gray-500'),
                    box('Reading time', style='text-sm font-medium text-gray-600'),
                ),
                style='mt-6'),
            box(style='absolute inset-x-0 bottom-0 h-2  bg-gradient-to-r from-green-300 via-blue-500 to-purple-600'),
            style='relative p-8 overflow-hidden border border-gray-100 rounded-lg',
        ),
        style='w-96',
    )
