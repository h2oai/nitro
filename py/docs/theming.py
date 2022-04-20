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

# ## Theme Switching
# Themes can be switched dynamically. This is useful when end-users need to switch the app's theme.
#
# Use `view.set(theme=)` to set the theme.
#
# Use `Theme()` to define a theme.
# - `background_color` sets the color of the page background.
# - `foreground_color` sets the color of the page text.
# - `accent_color` sets the accent color.
# - `accent_color_name` sets the closest matching named color. Must be one of `red`, `lava`, `orange`, `amber`,
#   `yellow`, `lime`, `mint`, `green`, `teal`, `cyan`, `sky`, `blue`, `indigo`, `purple`, `violet`, or `pink`.
#   This is used to pick spectrum colors, useful for visualizations and infographics.
def theme_switching(view: View):
    action = view(box(dict(change='Change my theme', dont_change='Done')))
    if action == 'change':
        view.set(theme=Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#ef534f',
            accent_color_name='red'
        ))


# ## Color Variables
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
    style = dict(width='35px', height='35px', border='#777', margin='0 0 2.5rem 0')
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


# ## Sample themes
# This example provides several sample themes that you can use in your own app.
def theme_samples(view: View):
    themes = {
        'Red': Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#ef534f',
            accent_color_name='red'
        ),
        'Dark Red': Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#ef534f',
            accent_color_name='red'
        ),
    }

    while True:
        theme, action = view(
            box('Change theme to:', mode='radio', options=list(themes.keys())),
            box(['Apply', 'Done'])
        )
        if action == 'Done':
            break
        view.set(theme=themes.get(theme))
