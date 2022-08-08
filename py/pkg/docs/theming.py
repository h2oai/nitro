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


# ## Use color variables
# *Color variables* are pre-defined, named colors that match the app's theme.
#
# Color variables take the form `var(--name)`, or simply `$name`. For example, you can use
# `var(--red)` or `$red` instead of hard-coded colors like `red` or `#ff0000` or `rgb(255,0,0)`.
#
# Color variables can be passed wherever colors are accepted, like `background=`, `border=`, `color=`, and so on.
#
# There are 16 pre-defined *spectrum colors*, derived automatically from the theme's accent color by matching its
# saturation and lightness. Spectrum colors are useful for data visualizations and infographics. The naming of each
# color is only indicative, and its hue might appear off depending on the position of the accent color's hue along the
# color spectrum. For example, `$red` could appear pink or orange!
#
# Additionally, there are pre-defined color variables for various *tones* of the theme's foreground (`$foreground`),
# background (`$background`) and accent (`$accent`) colors.
# Accent tones are prefixed with `$accent-`, and neutral tones (grays) are prefixed with `$neutral-`.
def theme_colors(view: View):
    style = dict(width=30, height=30, border='#777', margin='0 0 2.5rem 0')
    view(
        '### Spectrum Colors',
        row(
            box(background='$red', **style),
            box(background='$lava', **style),
            box(background='$orange', **style),
            box(background='$amber', **style),
            box(background='$yellow', **style),
            box(background='$lime', **style),
            box(background='$mint', **style),
            box(background='$green', **style),
            box(background='$teal', **style),
            box(background='$cyan', **style),
            box(background='$sky', **style),
            box(background='$blue', **style),
            box(background='$indigo', **style),
            box(background='$purple', **style),
            box(background='$violet', **style),
            box(background='$pink', **style),
            wrap='normal',
        ),
        '### Theme Colors',
        row(
            box(background='$foreground', **style),
            box(background='$background', **style),
            box(background='$accent', **style),
            wrap='normal',
        ),
        '### Accent Tones',
        row(
            box(background='$accent-darker', **style),
            box(background='$accent-dark', **style),
            box(background='$accent-dark-alt', **style),
            box(background='$accent-primary', **style),
            box(background='$accent-secondary', **style),
            box(background='$accent-tertiary', **style),
            box(background='$accent-light', **style),
            box(background='$accent-lighter', **style),
            box(background='$accent-lighter-alt', **style),
            wrap='normal',
        ),
        '### Neutral Tones',
        row(
            box(background='$neutral-dark', **style),
            box(background='$neutral-primary', **style),
            box(background='$neutral-primary-alt', **style),
            box(background='$neutral-secondary', **style),
            box(background='$neutral-secondary-alt', **style),
            box(background='$neutral-tertiary', **style),
            box(background='$neutral-tertiary-alt', **style),
            box(background='$neutral-quaternary', **style),
            box(background='$neutral-quaternary-alt', **style),
            box(background='$neutral-light', **style),
            box(background='$neutral-lighter', **style),
            box(background='$neutral-lighter-alt', **style),
            wrap='normal',
        ),
    )


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
