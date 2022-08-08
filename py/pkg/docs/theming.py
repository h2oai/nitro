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

from h2o_nitro import View, box, row, col, option, lorem, Theme


# # Theming
# Learn how to customize your app's color scheme.

# ## Set initial theme
# To set the theme, set `theme=Theme(mode, accent)` when creating the app's `View()`.
#
# `mode` sets the color scheme for prose, and `accent` sets the accent color for UI components.
#
# - For light mode, set `mode` to one of `light` (default), `light gray`, `light slate`, `light zinc`, `light neutral`, or `light stone`.
# - For dark mode, set `mode` to one of `dark` (default), `dark gray`, `dark slate`, `dark zinc`, `dark neutral`, or `dark stone`.
#
# `light` is shorthand for `light gray`, and `dark` is shorthand for `dark gray`.
# The colors `gray`, `slate`, `zinc`, `neutral`, and `stone` indicate the text color. The background color for dark mode is automatically chosen for you.
#
# `accent` must be one of `red`, `orange`, `amber`, `yellow`, `lime`, `green`, `emerald`, `teal`, 
# `cyan`, `sky`, `blue`, `indigo`, `violet`, `purple`, `fuchsia`, `pink`, `rose`, `slate`, `gray`, 
# `zinc`, `neutral`, or `stone`.

def theme_basic_noop(view: View):
    # App entry point
    def main(view: View):
        pass

    # Create theme
    my_theme = Theme(
        mode='dark zinc',
        accent='indigo',
    )

    # Set theme when creating the View()
    nitro = View(main, title='My App', caption='v1.0', theme=my_theme)

    view()


# ## Switch themes dynamically
# Call `view.set(theme=Theme(...))` to change the theme dynamically.
#
# The example below switches between light and dark modes.
def theme_dark_mode(view: View):  # height 12
    dark_mode = False
    while True:
        response = view(
            box('Dark Mode', mode='toggle', value=dark_mode),
            # Sample text
            '## This is not a drill',
            lorem(5),
            # Sample fields
            box('Enter text', placeholder='Enter some text'),
            box('Enter a number', value=42),
            box('Check this', mode='check', value=True),
            box('Toggle this', mode='toggle', value=True),
            box('Are you sure?', mode='radio', options=['Yes', 'No']),
            box('Pick a flavor', mode='menu', options=['Chocolate', 'Vanilla'], value='Chocolate'),
            box('Pick a value', mode='range', value=42, range=(0, 100)),
            box('Pick a day', mode='day'),
            box('Rate this', mode='rating'),
            box(["Let's go!", 'Not now']),
            style='p-4'
        )
        dark_mode = response[0]
        view.set(theme=Theme(mode='dark' if dark_mode else 'light'))


# ## Prose color sampler
# The example below shows all the prose theme variations.
def theme_prose_modes(view: View):  # height 5
    modes = [
        'light', 'dark',
        'light gray', 'light slate', 'light zinc', 'light neutral', 'light stone',
        'dark gray', 'dark slate', 'dark zinc', 'dark neutral', 'dark stone',
    ]

    sample_text = f'## {lorem()}\n### {lorem()}\n{lorem(5)}\n### {lorem()}\n{lorem(5)}'

    mode = modes[0]
    while True:
        mode = view(
            box('Mode', mode='live menu', options=modes, value=mode),
            sample_text,
            style='p-4'
        )
        view.set(theme=Theme(mode=mode))


# ## Color palette
# Use the following code to reproduce the entire active color palette for reference.
def theme_colors(view: View):  # height 15
    shades = '50 100 200 300 400 500 600 700 800 900'.split()
    accents = [
        'red', 'orange', 'amber', 'yellow', 'lime', 'green', 'emerald', 'teal', 'cyan',
        'sky', 'blue', 'indigo', 'violet', 'purple', 'fuchsia', 'pink', 'rose',
    ]

    def swatch(color, shade):
        return box(
            box(style=f'rounded w-14 h-10 bg-{color}-{shade}'),
            box(shade, style='text-xs font-medium'),
        )

    def swatches(color):
        return row(
            box(color, style='w-16 text-sm font-semibold'),
            row(*[swatch(color, shade) for shade in shades])
        )

    return view(*[swatches(color) for color in accents])


# ## Accent color styles
# To apply the active accent color, use `accent` as the name of the color.
#
# For example, if you've set the theme's accent color to `indigo`, you can use `bg-accent-500` instead of
# `bg-indigo-500` to change the background color of a box.
def theme_accent_colors(view: View):  # height 3

    def swatch(shade):
        return box(
            box(style=f'rounded h-10 bg-accent-{shade}'),
            box(f'accent-{shade}', style='text-xs font-medium'),
        )

    accents = [
        'red', 'orange', 'amber', 'yellow', 'lime', 'green', 'emerald', 'teal', 'cyan',
        'sky', 'blue', 'indigo', 'violet', 'purple', 'fuchsia', 'pink', 'rose',
    ]
    shades = '50 100 200 300 400 500 600 700 800 900'.split()
    swatches = [swatch(shade) for shade in shades]
    accent = 'indigo'

    while True:
        accent = view(
            box('Accent color', mode='live menu', value=accent, options=accents),
            box(*swatches, style='grid grid-cols-5 gap-2'),
        )
        view.set(theme=Theme(mode='light', accent=accent))


# ## Accent color sampler
# This example provides some sample themes that you can use in your own app.
def theme_samples(view: View):  # height 11
    accents = [
        'red', 'orange', 'amber', 'yellow', 'lime', 'green', 'emerald', 'teal', 'cyan',
        'sky', 'blue', 'indigo', 'violet', 'purple', 'fuchsia', 'pink', 'rose',
    ]
    accent = accents[0]
    dark_mode = False
    while True:
        response = view(
            row(
                box('Accent color', mode='live menu', value=accent, options=accents),
                box('Dark Mode', mode='toggle', value=dark_mode),
                style='items-end'
            ),
            # Sample fields
            box('Preview', mode='separator'),
            box('Enter text', placeholder='Enter some text'),
            box('Enter a number', value=42),
            box('Check this', mode='check', value=True),
            box('Toggle this', mode='toggle', value=True),
            box('Are you sure?', mode='radio', options=['Yes', 'No']),
            box('Pick a flavor', mode='menu', options=['Chocolate', 'Vanilla'], value='Chocolate'),
            box('Pick a value', mode='range', value=42, range=(0, 100)),
            box('Pick a day', mode='day'),
            box('Rate this', mode='rating'),
            box(["Let's go!", 'Not now']),
            style='p-4',
        )
        accent = response[0]
        dark_mode = response[1]
        view.set(theme=Theme(mode='dark' if dark_mode else 'light', accent=accent))
