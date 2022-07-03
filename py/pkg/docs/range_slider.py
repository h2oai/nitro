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


# # Range Slider
# Use range sliders to allow picking a numeric range within a given range.

# ## Basic
# Set `value=` to a `(start, end)` tuple to show a range slider.
#
# The mode setting `mode='range'` is implied, and can be elided.
def range_slider_basic(view: View):  # height 2
    start, end = view(box('Speed range (km/h)', value=(3, 7)))
    view(f'Your speed ranges between {start} and {end} km/h')


# ## Set min value
# Set `min=` to specify a minimum value.
def range_slider_min(view: View):  # height 2
    start, end = view(box('Speed range (km/h)', value=(3, 7), min=3))
    view(f'Your speed ranges between {start} and {end} km/h')


# ## Set max value
# Set `max=` to specify a maximum value.
def range_slider_max(view: View):  # height 2
    start, end = view(box('Speed range (km/h)', value=(30, 70), max=100))
    view(f'Your speed ranges between {start} and {end} km/h')


# ## Set step
# Set `step=` to specify how much to increment or decrement by.
#
# The default step is `1`.
def range_slider_step(view: View):  # height 2
    start, end = view(box('Speed range (km/h)', value=(2, 6), step=2))
    view(f'Your speed ranges between {start} and {end} km/h')


# ## Set precision
# Set `precision=` to specify how many decimal places the value should be rounded to.
#
# The default is calculated based on the precision of step:
# - if step = 1, precision = 0
# - if step = 0.42, precision = 2
# - if step = 0.0042, precision = 4
def range_slider_precision(view: View):  # height 2
    start, end = view(box('Speed range (m/s)', value=(-0.4, 0.4), min=-2, max=2, step=0.2, precision=2))
    view(f'Your speed ranges between {start} and {end} m/s')


# ## Combine min, max, step, precision
# `min=`, `max=`, `step=` and `precision=` can be combined.
def range_slider_range(view: View):  # height 2
    start, end = view(box('Speed range (km/h)', value=(30, 70), min=10, max=100, step=5))
    view(f'Your speed ranges between {start} and {end} km/h')


# ## Set range
# Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def range_slider_range_alt(view: View):  # height 2
    start, end = view(box('Speed range (km/h)', value=(30, 70), range=(10, 100)))
    view(f'Your speed ranges between {start} and {end} km/h')


# ## Set range with step
# Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.
#
# This is a shorthand notation for setting `min=`, `max=` and `step` individually.
def range_slider_range_alt_step(view: View):  # height 2
    start, end = view(box('Speed range (km/h)', value=(30, 70), range=(10, 100, 5)))
    view(f'Your speed ranges between {start} and {end} km/h')


# ## Set range with precision
# Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.
# Setting `range=` to a `(min, max, step, precision)` tuple is shorthand for setting
# `min=`, `max=`, `step` and `precision` individually.
def range_slider_range_alt_precision(view: View):  # height 2
    start, end = view(box('Speed range (m/s)', value=(-0.4, 0.4), range=(-2, 2, 0.2, 2)))
    view(f'Your speed ranges between {start} and {end} m/s')


# ## Use zero-crossing range
# Ranges can cross zero.
def range_slider_negative(view: View):  # height 2
    start, end = view(box('Speed range (m/s)', value=(-3, 3), range=(-5, 5)))
    view(f'Your speed ranges between {start} and {end} m/s')


# ## Set fractional steps
# Steps can be fractional.
def range_slider_decimal_step(view: View):  # height 2
    start, end = view(box('Speed range (m/s)', value=(-0.4, 0.4), range=(-2, 2, 0.2)))
    view(f'Your speed ranges between {start} and {end} m/s')


# ## Capture changes immediately
# Set `live=True` to immediately capture changes to the range slider.
def range_slider_live(view: View):  # height 2
    start, end = 3, 7  # Starting values
    while True:
        start, end = view(
            box('Speed range (km/h)', value=(start, end), live=True),
            box(f'Your speed ranges between {start} and {end} km/h'),
        )
