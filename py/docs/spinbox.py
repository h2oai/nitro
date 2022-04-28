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


# # Spinbox

# ## Basic
# Call `box()` with `mode='number'` to show a box with increment/decrement buttons.
# (also called a *spinbox*).
def spinbox_basic(view: View):
    speed = view(box('Speed (km/h)', mode='number'))
    view(f'Your speed is {speed} km/h')


# ## Set initial value
# Set `value=` to a numeric value to prefill the box with the value.
#
# The mode setting `mode='number'` is implied, and can be elided.
def spinbox_value(view: View):
    speed = view(box('Speed (km/h)', value=42))
    view(f'Your speed is {speed} km/h')


# In other words, calling `box()` with a numeric `value` has the same effect
# as setting `mode='number'`, and is the preferred usage.

# ## Set min value
# Set `min=` to specify a minimum value.
def spinbox_min(view: View):
    speed = view(box('Speed (km/h)', min=10))
    view(f'Your speed is {speed} km/h')


# ## Set max value
# Set `max=` to specify a maximum value.
def spinbox_max(view: View):
    speed = view(box('Speed (km/h)', max=100))
    view(f'Your speed is {speed} km/h')


# ## Set step
# Set `step=` to specify how much to increment or decrement by.
#
# The default step is `1`.
def spinbox_step(view: View):
    speed = view(box('Speed (km/h)', step=5))
    view(f'Your speed is {speed} km/h')


# ## Set precision
# Set `precision=` to specify how many decimal places the value should be rounded to.
#
# The default is calculated based on the precision of step:
#
# - if step = 1, precision = 0
# - if step = 0.42, precision = 2
# - if step = 0.0042, precision = 4
def spinbox_precision(view: View):
    speed = view(box('Speed (m/s)', value=0.6, min=-2, max=2, step=0.2, precision=2))
    view(f'Your speed is {speed} m/s')


# ## Combine min, max, step, precision
# `min=`, `max=`, `step=` and `precision=` can be combined.
def spinbox_range(view: View):
    speed = view(box('Speed (km/h)', min=10, max=100, step=5))
    view(f'Your speed is {speed} km/h')


# ## Set range
# Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def spinbox_range_alt(view: View):
    speed = view(box('Speed (km/h)', range=(10, 100)))
    view(f'Your speed is {speed} km/h')


# ## Set range with step
# Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.
#
# This is a shorthand notation for setting `min=`, `max=` and `step` individually.
def spinbox_range_alt_step(view: View):
    speed = view(box('Speed (km/h)', range=(10, 100, 5)))
    view(f'Your speed is {speed} km/h')


# ## Set range with precision
# Setting `range=` to a `(min, max, step, precision)` tuple is a shorthand notation for setting
# `min=`, `max=`, `step` and `precision` individually.
def spinbox_range_alt_precision(view: View):
    speed = view(box('Speed (m/s)', value=0.6, range=(-2, 2, 0.2, 2)))
    view(f'Your speed is {speed} m/s')


# ## Use zero-crossing ranges
# Ranges can cross zero.
def spinbox_negative(view: View):
    speed = view(box('Speed (m/s)', value=-3, range=(-5, 5)))
    view(f'Your speed is {speed} m/s')


# ## Use fractional steps
# Steps can be fractional.
def spinbox_decimal_step(view: View):
    speed = view(box('Speed (m/s)', value=0.6, range=(-2, 2, 0.2)))
    view(f'Your speed is {speed} m/s')
