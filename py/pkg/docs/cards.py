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
def card_basic(view: View):
    icon = '''
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
    </svg>
    '''

    def card(title, caption, score):
        return box(
            box(score,
                style='absolute top-4 right-4 rounded-full px-3 py-1.5 bg-green-100 text-green-600 font-medium text-xs'),
            col(
                box(icon, mode='svg', style='w-10 h-10'),
                box(title, style='text-xl font-bold text-gray-900'),
                box(caption, style='text-sm'),
                style='text-gray-500 pr-8',
            ),
            style='relative p-8 border shadow hover:shadow-xl rounded-xl',
        )

    view(
        box(
            card(lorem(), lorem(2), '4.2'),
            card(lorem(), lorem(2), '2.6'),
            card(lorem(), lorem(2), '3.9'),
            card(lorem(), lorem(2), '5.0'),
            style='grid grid-cols-2 grid-rows-2 gap-4',
        )
    )


# ## With gradient border
def card_gradient_border(view: View):
    def card(title, caption):
        return box(
            box(
                box(
                    box(title, style='text-xl font-bold text-gray-900'),
                    box(caption, style='mt-2 text-sm text-gray-500'),
                    style='mt-16 pr-8',
                ),
                style='absolute inset-1 bg-white p-8 rounded-xl'
            ),
            style='relative h-72 shadow-xl bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500 rounded-2xl',
        )

    view(
        box(
            card(lorem(), lorem(2)),
            card(lorem(), lorem(2)),
            card(lorem(), lorem(2)),
            card(lorem(), lorem(2)),
            style='grid grid-cols-2 grid-rows-2 gap-4',
        )
    )

