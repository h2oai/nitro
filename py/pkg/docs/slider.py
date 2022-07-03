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


# # Slider
# Use sliders to allow picking a number in a given range.

# ## Basic
# Set `mode='range'` to show a slider.
#
# The default range is between `0` and `10`.
def slider_basic(view: View):  # height 2
    speed = view(box('Speed (km/h)', mode='range'))
    view(f'Your speed is {speed} km/h')


# ## Set initial value
# Set `value=` to default the slider value.
def slider_value(view: View):  # height 2
    speed = view(box('Speed (km/h)', mode='range', value=5))
    view(f'Your speed is {speed} km/h')


# ## Capture changes immediately
# Set `live=True` to immediately capture changes to the slider.
def slider_live(view: View):  # height 2
    speed = 5  # Starting value
    while True:
        speed = view(
            box('Speed (km/h)', mode='range', value=speed, live=True),
            box(f'Your speed is {speed} km/h'),
        )


# ## Set min value
# Set `min=` to specify a minimum value.
def slider_min(view: View):  # height 2
    speed = view(box('Speed (km/h)', mode='range', min=3))
    view(f'Your speed is {speed} km/h')


# ## Set max value
# Set `max=` to specify a maximum value.
def slider_max(view: View):  # height 2
    speed = view(box('Speed (km/h)', mode='range', max=100))
    view(f'Your speed is {speed} km/h')


# ## Set step
# Set `step=` to specify how much to increment or decrement by.
#
# The default step is `1`.
def slider_step(view: View):  # height 2
    speed = view(box('Speed (km/h)', mode='range', step=2))
    view(f'Your speed is {speed} km/h')


# ## Set precision
# Set `precision=` to specify how many decimal places the value should be rounded to.
#
# The default is calculated based on the precision of step:
#
# - if step = 1, precision = 0
# - if step = 0.42, precision = 2
# - if step = 0.0042, precision = 4
def slider_precision(view: View):  # height 2
    speed = view(box('Speed (m/s)', mode='range', value=0.6, min=-2, max=2, step=0.2, precision=2))
    view(f'Your speed is {speed} m/s')


# ## Combine min, max, step, precision
# `min=`, `max=`, `step=` and `precision=` can be combined.
def slider_range(view: View):  # height 2
    speed = view(box('Speed (km/h)', mode='range', min=10, max=100, step=5))
    view(f'Your speed is {speed} km/h')


# ## Set range
# Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def slider_range_alt(view: View):  # height 2
    speed = view(box('Speed (km/h)', mode='range', range=(10, 100)))
    view(f'Your speed is {speed} km/h')


# ## Set range with step
# Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.
#
# This is a shorthand notation for setting `min=`, `max=` and `step` individually.
def slider_range_alt_step(view: View):  # height 2
    speed = view(box('Speed (km/h)', mode='range', range=(10, 100, 5)))
    view(f'Your speed is {speed} km/h')


# ## Set range with precision
# Setting `range=` to a `(min, max, step, precision)` tuple is shorthand setting
# `min=`, `max=`, `step` and `precision` individually.
def slider_range_alt_precision(view: View):  # height 2
    speed = view(box('Speed (m/s)', mode='range', value=0.6, range=(-2, 2, 0.2, 2)))
    view(f'Your speed is {speed} m/s')


# ## Zero-crossing range
# Ranges can cross zero.
def slider_negative(view: View):  # height 2
    speed = view(box('Speed (m/s)', mode='range', value=-3, range=(-5, 5)))
    view(f'Your speed is {speed} m/s')


# ## Set fractional steps
# Steps can be fractional.
def slider_decimal_step(view: View):  # height 2
    speed = view(box('Speed (m/s)', mode='range', value=0.6, range=(-2, 2, 0.2)))
    view(f'Your speed is {speed} m/s')
