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


# # Theming

# ## Color Variables
# To use pre-defined, named colors that sit well with the app's theme, use *color variables*.
# Color variables take the form `var(--name)` or simply `$name`.
# For example, you can use `var(--red)` or `$red` instead of hard-coded colors like `red` or `#ff0000` or `rgb(255,0,0)`.
#
# Color variables can be passed wherever colors are accepted, like `background`, `border`, `color`, and so on.
#
# There are 16 pre-defined *spectrum colors*, derived automatically from the theme's accent color, by matching its
# saturation and lightness. The naming of each color is indicative, and its hue might appear off depending on the
# position of the accent color's hue along the color spectrum. For example, `$red` could appear pink or orange!
#
# Additionally, there are pre-defined color variables for various *tones* of the theme's foreground (`$foreground`),
# background (`$background`) and accent (`$accent`) colors.
# Accent color tones are prefixed with `$accent-`, and neutral tones (grays) are prefixed with `$neutral-`.
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
