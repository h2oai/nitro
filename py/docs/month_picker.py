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


# # Month Picker

# ## Basic
# Set `mode='month'` to show a month picker.
def month_basic(view: View):
    month = view(box('Pick a month', mode='month'))
    view(f'You picked {month}.')


# ## Value
# Set `value=` to pre-select a month.
#
# Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
# Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.
def month_value(view: View):
    month = view(box('Pick a month', mode='month', value='2021-10-10'))
    view(f'You picked {month}.')


# ## Min
# Set `min=` to specify a minimum date.
def month_min(view: View):
    month = view(box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01'))
    view(f'You picked {month}.')


# ## Max
# Set `max=` to specify a maximum date.
def month_max(view: View):
    month = view(box('Pick a month', mode='month', value='2021-10-10', max='2022-12-31'))
    view(f'You picked {month}.')


# ## Min and Max
# Set both `min=` and `max=` to restrict selection between two dates.
def month_min_max(view: View):
    month = view(box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
    view(f'You picked {month}.')


# ## Range
# Set `range=` to a `(min, max)` tuple to restrict selection between two dates.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def month_range(view: View):
    month = view(box('Pick a month', mode='month', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    view(f'You picked {month}.')
