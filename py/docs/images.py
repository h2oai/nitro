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


# # Images

# ## Basic
# Set `image=` to display an image.
def image_basic(view: View):
    view(box(image='sample.jpg'))


# Photo by [Ju Guan](https://unsplash.com/@guanju223?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).

# ## Set width and height
# Images can be resized by setting `width=` or `height=` or both.
#
# - If only `width=` or only `height=` are set, the image is scaled proportionally.
# - If both `width=`and`height=`are set, the image is stretched to fit, and might appear distorted.
def image_resize(view: View):
    view(
        box(image='sample.jpg', width=300),
        box(image='sample.jpg', height=200),
        box(image='sample.jpg', width=150, height=300),
    )


# ## Scale and clip images
# Set `fit=` to control how the image should be resized to fit its box.
#
# - `fit='cover'` (default) scales and *clips* the image while preserving its aspect ratio.
# - `fit='contain'` scales and *letterboxes* the image while preserving its aspect ratio.
# - `fit='fill'` stretches the image to fit.
# - `fit='none'` clips the image without resizing.
# - `fit='scale-down'` behaves like either `contain` or `none`, whichever results in a smaller image.
def image_fit(view: View):
    style = dict(width=100, height=200)
    view(
        row(
            box(image='sample.jpg', fit='cover', **style),
            box(image='sample.jpg', fit='contain', **style),
            box(image='sample.jpg', fit='fill', **style),
            box(image='sample.jpg', fit='none', **style),
            box(image='sample.jpg', fit='scale-down', **style),
        )
    )


# ## Use as background
# If a box contains content, its image is used as a background.
#
# Set `fit=` to control how the background should be resized to fit the box.
def image_background(view: View):
    style = dict(width=100, height=200, color='white')
    view(
        row(
            box('Astro', image='sample.jpg', **style),
            box('Astro', image='sample.jpg', fit='cover', **style),
            box('Astro', image='sample.jpg', fit='contain', **style),
            box('Astro', image='sample.jpg', fit='fill', **style),
            box('Astro', image='sample.jpg', fit='none', **style),
            image='sample.jpg',  # A background for the row as well!
        )
    )


# ## Use as pattern
# `image=` can also be set to a [Data URI](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs)
# with a [base64-encoded](https://en.wikipedia.org/wiki/Base64) image.
#
# The example below uses `fit='none'` to repeat a small PNG tile horizontally and vertically to form a pattern.
def image_background_pattern(view: View):
    view(box(
        '# Patterns!',
        image='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAEUlEQVQIHWNggIBiEGUFxJUABisBJ85jLc8AAAAASUVORK5CYII=',
        fit='none', height=300
    ))
