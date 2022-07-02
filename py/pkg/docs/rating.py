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


# # Rating
# Use a rating component to capture a star-rating.

# ## Basic
# Set `mode='rating'` to accept a star-rating.
#
# By default, five stars are displayed.
def rating_basic(view: View):  # height 2
    stars = view(box('Rate your experience', mode='rating'))
    view(f'Your rating was {stars} stars.')


# ## Set initial rating
# Set `value=` to specify a default value.
def rating_value(view: View):  # height 2
    stars = view(box('Rate your experience', mode='rating', value=3))
    view(f'Your rating was {stars} stars.')


# ## Allow zero stars
# Set `min=0` to allow zero stars.
def rating_min(view: View):  # height 2
    stars = view(box('Rate your experience', mode='rating', min=0))
    view(f'Your rating was {stars} stars.')


# ## Set maximum number of stars
# Set `max=` to increase the number of stars displayed.
def rating_max(view: View):  # height 2
    stars = view(box('Rate your experience', mode='rating', value=3, max=10))
    view(f'Your rating was {stars} stars.')


# ## Combine min and max stars
# `min=` and `max=` can be combined.
def rating_min_max(view: View):  # height 2
    stars = view(box('Rate your experience', mode='rating', value=3, min=0, max=10))
    view(f'Your rating was {stars} stars.')


# ## Set range
# Set `range=` to a `(min, max)` tuple to control min/max stars.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def rating_range(view: View):  # height 2
    stars = view(box('Rate your experience', mode='rating', value=3, range=(0, 10)))
    view(f'Your rating was {stars} stars.')
