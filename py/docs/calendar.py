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


# # Calendar

# ## Basic

# Set `mode='day'` to show a calendar.
def day_basic(view: View):
    date = view(box('Pick a date', mode='day'))
    view(f'You picked {date}.')


# ## Value
# Set `value=` to pre-select a date.
#
# Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
# Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.
def day_value(view: View):
    date = view(box('Pick a date', mode='day', value='2021-10-10'))
    view(f'You picked {date}.')


# ## Min
# Set `min=` to specify a minimum date.
def day_min(view: View):
    date = view(box('Pick a date', mode='day', value='2021-10-10', min='2019-01-01'))
    view(f'You picked {date}.')


# ## Max
# Set `max=` to specify a maximum date.
def day_max(view: View):
    date = view(box('Pick a date', mode='day', value='2021-10-10', max='2022-12-31'))
    view(f'You picked {date}.')


# ## Min and Max
# Set both `min=` and `max=` to restrict selection between two dates.
def day_min_max(view: View):
    date = view(box('Pick a date', mode='day', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
    view(f'You picked {date}.')


# ## Range
# Set `range=` to a `(min, max)` tuple to restrict selection between two dates.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def day_range(view: View):
    date = view(box('Pick a date', mode='day', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    view(f'You picked {date}.')
