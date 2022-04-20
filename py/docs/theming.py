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

# ## Setting a theme
# Pass `theme=` when creating the app's `View()`.
#
# Use `Theme()` to define a theme.
# - `background_color` sets the color of the page background.
# - `foreground_color` sets the color of the page text.
# - `accent_color` sets the accent color.
# - `accent_color_name` describes the accent color.
#
# `accent_color_name` must be one of `red`, `lava`, `orange`, `amber`, `yellow`, `lime`, `mint`, `green`, `teal`,
# `cyan`, `sky`, `blue`, `indigo`, `purple`, `violet`, or `pink`.
# This is used to automatically pick matching spectrum colors, useful for visualizations and infographics.
def theme_basic(view: View):
    # App entry point
    def main(view: View):
        pass

    # Create theme
    my_theme = Theme(
        background_color='#fff',
        foreground_color='#3e3f4a',
        accent_color='#ef534f',
        accent_color_name='green'
    )

    # Set theme when creating the View()
    nitro = View(main, title='My App', caption='v1.0', theme=my_theme)

    view()


# ## Theme Switching
# Use `view.set(theme=)` to change the theme dynamically.
#
# This is useful when you want to allow the app's end-users to switch app's theme.
def theme_switching(view: View):
    make_red = False
    while True:
        make_red, done = view(
            box('Apply red theme', mode='toggle', value=make_red),
            box(['Done'])
        )

        if done:
            break

        if make_red:
            view.set(theme=Theme(
                background_color='#fff',
                foreground_color='#3e3f4a',
                accent_color='#ef534f',
                accent_color_name='red'
            ))
        else:
            view.set(theme=Theme(
                background_color='#fff',
                foreground_color='#3e3f4a',
                accent_color='#5a64f0',
                accent_color_name='indigo'
            ))


# ## Dark mode
# A simple way to allow switching between dark and light modes is to exchange the `background_color` and
# `foreground_color` in the theme, provided the `accent_color` works with both dark and light backgrounds.
def theme_dark_mode(view: View):
    dark_mode = False
    while True:
        dark_mode, done = view(
            box('Dark Mode', mode='toggle', value=dark_mode),
            box(['Done'])
        )

        if done:
            break

        if dark_mode:
            view.set(theme=Theme(
                background_color='#3e3f4a',  # dark background
                foreground_color='#fff',  # light foreground
                accent_color='#ef534f',
                accent_color_name='red'
            ))
        else:
            view.set(theme=Theme(
                background_color='#fff',  # light background
                foreground_color='#3e3f4a',  # dark foreground
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
# This example provides some sample themes that you can use in your own app.
def theme_samples(view: View):
    themes = [
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#ef5350',
            accent_color_name='red',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#ec407a',
            accent_color_name='pink',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#ab47bc',
            accent_color_name='violet',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#7e57c2',
            accent_color_name='purple',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#5c6bc0',
            accent_color_name='indigo',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#42a5f5',
            accent_color_name='blue',
        ),
        Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#29b6f6',
            accent_color_name='sky',
        ),
        Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#26c6da',
            accent_color_name='cyan',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#26a69a',
            accent_color_name='teal',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#66bb6a',
            accent_color_name='green',
        ),
        Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#9ccc65',
            accent_color_name='mint',
        ),
        Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#d4e157',
            accent_color_name='lime',
        ),
        Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#ffee58',
            accent_color_name='yellow',
        ),
        Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#ffca28',
            accent_color_name='amber',
        ),
        Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#ffa726',
            accent_color_name='orange',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#ff7043',
            accent_color_name='lava',
        ),
    ]

    theme_lookup = {theme.accent_color_name: theme for theme in themes}
    theme_names = list(theme_lookup.keys())
    theme_names.sort()
    theme_name = theme_names[0]

    while True:
        theme_name, action = view(
            box('Pick a theme', value=theme_name, options=theme_names, ),
            box(['Apply', 'Done'])
        )
        if action == 'Done':
            break
        view.set(theme=theme_lookup.get(theme_name))
