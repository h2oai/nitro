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
# Pass `theme=` when creating the app's `View()`.
#
# Use `Theme()` to define a theme.
# - `background_color` sets the color of the page background.
# - `foreground_color` sets the color of the page text.
# - `accent_color` sets the accent color.
def theme_basic_noop(view: View):
    # App entry point
    def main(view: View):
        pass

    # Create theme
    my_theme = Theme(
        background_color='#fff',  # white
        foreground_color='#3f3f46',  # zinc-700
        accent_color='#ef4444',  # red-500
    )

    # Set theme when creating the View()
    nitro = View(main, title='My App', caption='v1.0', theme=my_theme)

    view()


# ## Switch theme dynamically
# Use `view.set(theme=)` to change the theme dynamically.
#
# This is useful when you want to allow the app's end-users to switch app's theme.
def theme_switching(view: View):  # height 2
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
                background_color='#fff',  # white
                foreground_color='#3f3f46',  # zinc-700
                accent_color='#ef4444',  # red-500
            ))
        else:
            view.set(theme=Theme(
                background_color='#fff',  # white
                foreground_color='#3f3f46',  # zinc-700
                accent_color='#6366f1',  # indigo-500
            ))


# ## Dark mode
# A simple way to allow switching between dark and light modes is to exchange the `background_color` and
# `foreground_color` in the theme, provided the `accent_color` works with both dark and light backgrounds.
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
        view.set(theme=Theme(
            background_color='#3f3f46' if dark_mode else '#fff',
            foreground_color='#fff' if dark_mode else '#3f3f46',
            accent_color='#6366f1',  # indigo-500
        ))


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


# ## Some sample themes
# This example provides some sample themes that you can use in your own app.
def theme_samples(view: View):  # height 11
    themes = [
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#ef5350',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#ec407a',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#ab47bc',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#7e57c2',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#5c6bc0',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#42a5f5',
        ),
        Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#29b6f6',
        ),
        Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#26c6da',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#26a69a',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#66bb6a',
        ),
        Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#9ccc65',
        ),
        Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#d4e157',
        ),
        Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#ffee58',
        ),
        Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#ffca28',
        ),
        Theme(
            background_color='#3e3f4a',
            foreground_color='#fff',
            accent_color='#ffa726',
        ),
        Theme(
            background_color='#fff',
            foreground_color='#3e3f4a',
            accent_color='#ff7043',
        ),
    ]

    theme_lookup = {theme.accent_color: theme for theme in themes}
    theme_names = list(theme_lookup.keys())
    theme_names.sort()
    theme_name = theme_names[0]

    while True:
        response = view(
            box('Pick a theme', mode='color', value=theme_name, options=theme_names, live=True),
            col(
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
                box(["Let's go!", 'Not now'])
            ),
        )
        theme_name = response[0]
        view.set(theme=theme_lookup.get(theme_name))
