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
                style='items-center border rounded text-xs font-medium px-2.5 py-1.5',
            ),
            row(
                box('Status: ', style='text-gray-700'),
                box('System paused', style='text-amber-700'),
                style='items-center border rounded text-xs font-medium px-2.5 py-1.5',
            ),
            row(
                box('Status: ', style='text-gray-700'),
                box('System normal', style='text-green-700'),
                style='items-center border rounded text-xs font-medium px-2.5 py-1.5',
            ),
            row(
                box('Status: ', style='text-gray-700'),
                box('System overload', style='text-red-700'),
                style='items-center border rounded text-xs font-medium px-2.5 py-1.5',
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


# ## Alert with icon
def styling_alert_icons(view: View):
    text = lorem(3)
    info_icon = '''
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    '''
    warning_icon = '''
     <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
     </svg>
    '''
    success_icon = '''
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    '''
    critical_icon = '''
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M20.618 5.984A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016zM12 9v2m0 4h.01" />
    </svg>
    '''
    view(
        row(
            box(
                box(info_icon, mode='svg', style='w-5 h-5'),
                style='p-2 text-white bg-sky-600 rounded-full',
            ),
            col(
                box('Your system is up to date.', style='text-sm font-medium'),
                box(text, style='text-xs opacity-90'),
            ),
            style='items-center justify-between gap-4 p-4 text-sky-700 border rounded border-sky-200 bg-sky-50',
        ),
        row(
            box(
                box(warning_icon, mode='svg', style='w-5 h-5'),
                style='p-2 text-white bg-amber-600 rounded-full',
            ),
            col(
                box('A system update is available.', style='text-sm font-medium'),
                box(text, style='text-xs opacity-90'),
            ),
            style='items-center justify-between gap-4 p-4 text-amber-700 border rounded border-amber-200 bg-amber-50',
        ),
        row(
            box(
                box(success_icon, mode='svg', style='w-5 h-5'),
                style='p-2 text-white bg-green-600 rounded-full',
            ),
            col(
                box('System update successful!', style='text-sm font-medium'),
                box(text, style='text-xs opacity-90'),
            ),
            style='items-center justify-between gap-4 p-4 text-green-700 border rounded border-green-200 bg-green-50',
        ),
        row(
            box(
                box(critical_icon, mode='svg', style='w-5 h-5'),
                style='p-2 text-white bg-red-600 rounded-full',
            ),
            col(
                box('System update failed.', style='text-sm font-medium'),
                box(text, style='text-xs opacity-90'),
            ),
            style='items-center justify-between gap-4 p-4 text-red-700 border rounded border-red-200 bg-red-50',
        ),
    )


# ## Pagination
def styling_pagination(view: View):
    def link(text: str, selected: bool):
        color = 'text-white bg-indigo-600 border-indigo-600' if selected else 'border'
        return box(text, style=f'w-8 h-8 leading-8 text-center rounded {color}')

    links = [link(text, text == '2') for text in ['←', '1', '2', '3', '4', '5', '→']]
    view(
        row(*links, style='justify-center gap-1 text-xs font-medium')
    )


# ## Timeline
def styling_timeline(view: View):
    def step(number: str, label: str, is_current: bool = False):
        color = 'text-white bg-indigo-600' if is_current else 'bg-gray-100'
        return row(
            box(number, style=f'w-6 h-6 text-xs font-bold leading-6 text-center rounded-full {color}'),
            box(label, mode='box'),
            style='items-center p-2 bg-white',
        )

    view(
        box(
            box(style='absolute bg-gray-100 top-1/2 inset-x-0 h-0.5'),
            row(
                step('1', 'Cart'),
                step('2', 'Shipping', is_current=True),
                step('3', 'Payment'),
                step('4', 'Confirm'),
                style='relative justify-between text-sm font-medium text-gray-500',
            ),
            style='relative',
        ),
    )


# ## Stat
def styling_stat(view: View):
    def stat(label: str, value: str):
        return col(
            box(value, style='text-4xl font-extrabold text-indigo-600'),
            box(label, style='text-lg font-medium text-gray-500'),
            style='gap-0 px-4 py-8 text-center border rounded-lg'
        )

    view(
        box(
            stat('Donut Sales', '$4.2M'),
            stat('Flavors', '24'),
            stat('Locations', '89'),
            style='grid grid-cols-3 gap-2',
        )
    )


# ## Stat with icon
def styling_stat_icon(view: View):
    icon = '''
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
    </svg>
    '''
    view(
        box(
            row(
                box(
                    box(icon, mode='svg', style='w-8 h-8'),
                    style='p-3 text-indigo-600 bg-indigo-100 rounded-full',
                ),
                col(
                    box('$4.2M', style='text-2xl font-medium text-gray-900'),
                    box('Annual Donut Sales', style='text-sm text-gray-400'),
                    style='gap-0',
                ),
                style='items-center gap-4 p-6 bg-white border rounded-lg',
            ),
            row(
                col(
                    box('$4.2M', style='text-2xl font-medium text-gray-900'),
                    box('Annual Donut Sales', style='text-sm text-gray-400'),
                    style='gap-0',
                ),
                box(
                    box(icon, mode='svg', style='w-8 h-8'),
                    style='p-3 text-indigo-600 bg-indigo-100 rounded-full',
                ),
                style='items-center justify-between gap-4 p-6 bg-white border rounded-lg',
            ),
            style='grid grid-cols-2 gap-2',
        ),
    )


# ## Stat with change
def styling_stat_change(view: View):
    increase_icon = '''
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
    </svg>
    '''
    decrease_icon = '''
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
    </svg>
    '''
    view(
        box(
            col(
                box('Donut Sales', style='text-sm text-gray-400'),
                box('$452.2K', style='text-2xl font-medium text-gray-900'),
                row(
                    box(increase_icon, mode='svg', style='w-4 h-4 text-green-600'),
                    box('6.5%', style='font-medium'),
                    box('Since last month', style='text-gray-400'),
                    style='gap-1 mt-1 text-xs',
                ),
                style='gap-0 p-6 bg-white border rounded-lg',
            ),
            col(
                box('Donut Sales', style='text-sm text-gray-400'),
                box('$452.2K', style='text-2xl font-medium text-gray-900'),
                row(
                    box(decrease_icon, mode='svg', style='w-4 h-4 text-red-600'),
                    box('6.5%', style='font-medium'),
                    box('Since last month', style='text-gray-400'),
                    style='gap-1 mt-1 text-xs',
                ),
                style='gap-0 p-6 bg-white border rounded-lg',
            ),
            style='grid grid-cols-2 gap-2',
        ),
    )


# ## Stat with floating change
def styling_stat_change_floating(view: View):
    increase_icon = '''
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
    </svg>
    '''
    decrease_icon = '''
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
    </svg>
    '''
    view(
        box(
            row(
                box(
                    box('Donut Sales', style='text-sm text-gray-400'),
                    box('$452.2K', style='text-2xl font-medium text-gray-900'),
                ),
                row(
                    box(increase_icon, mode='svg', style='w-4 h-4'),
                    box('6.5%', style='text-xs font-medium'),
                    style='p-1 text-green-600 bg-green-100 rounded',
                ),
                style='items-start justify-between p-6 bg-white border rounded-lg',
            ),
            row(
                box(
                    box('Donut Sales', style='text-sm text-gray-400'),
                    box('$452.2K', style='text-2xl font-medium text-gray-900'),
                ),
                row(
                    box(decrease_icon, mode='svg', style='w-4 h-4'),
                    box('6.5%', style='text-xs font-medium'),
                    style='p-1 text-red-600 bg-red-100 rounded',
                ),
                style='items-start justify-between p-6 bg-white border rounded-lg',
            ),
            style='grid grid-cols-2 gap-2',
        ),
    )
