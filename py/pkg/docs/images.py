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
# Display images, or use them as backgrounds or in patterns.

# ## Basic
# Set `image=` to display an image.
def image_basic(view: View):
    view(box(image='sample.jpg'))


# Photo by [Ju Guan](https://unsplash.com/@guanju223?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).

# ## Scale and clip images
# Set the `object-` style to control how the image should be resized to fit its box.
#
# - `object-cover` (default) scales and *clips* the image while preserving its aspect ratio.
# - `object-fill` stretches the image to fit.
# - `object-contain` scales and *letterboxes* the image while preserving its aspect ratio.
# - `object-none` clips the image without resizing.
# - `object-scale-down` behaves like either `contain` or `none`, whichever results in a smaller image.
def image_fit(view: View):  # height 4
    view(
        row(
            box(image='sample.jpg', style='w-32 h-32 border object-cover'),
            box(image='sample.jpg', style='w-32 h-32 border object-fill'),
            box(image='sample.jpg', style='w-32 h-32 border object-contain'),
            box(image='sample.jpg', style='w-32 h-32 border object-none'),
            box(image='sample.jpg', style='w-32 h-32 border object-scale-down'),
        )
    )


# Photo by [Ju Guan](https://unsplash.com/@guanju223?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).


# ## Use as background
# If a box contains child items, `image=` is used as a background.
def image_background(view: View):  # height 4
    view(
        col(
            box(
                'To the galaxy and beyond',
                style='font-bold text-3xl text-center text-white',
            ),
            image='sample.jpg',
            style='h-64 justify-center bg-cover bg-center'
        )
    )


# Photo by [Ju Guan](https://unsplash.com/@guanju223?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).


# ## Use as pattern
# `image=` can also be set to a [Data URI](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs)
# with a [base64-encoded](https://en.wikipedia.org/wiki/Base64) image.
#
# The example below uses the image as a background pattern.
def image_background_pattern(view: View):  # height 5
    view(
        col(
            box(
                'To the galaxy and beyond',
                style='font-bold text-3xl text-center text-white',
            ),
            image='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAEUlEQVQIHWNggIBiEGUFxJUABisBJ85jLc8AAAAASUVORK5CYII=',
            style='h-64 justify-center'
        )
    )
