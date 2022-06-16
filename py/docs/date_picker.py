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


# # Date Picker

# ## Basic
# Set `mode='date'` to show a date-picker.
def date_basic(view: View):  # height 2
    date = view(box('Pick a date', mode='date'))
    view(f'You picked {date}.')


# ## Set initial date
# Set `value=` to pre-select a date.
#
# Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
# Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.
def date_value(view: View):  # height 2
    date = view(box('Pick a date', mode='date', value='2021-10-10'))
    view(f'You picked {date}.')


# ## Set placeholder text
# Set `placeholder=` to show placeholder text.
def date_placeholder(view: View):  # height 2
    date = view(box('Deliver on', mode='date', placeholder='Delivery date'))
    view(f'You picked {date}.')


# ## Set min date
# Set `min=` to specify a minimum date.
def date_min(view: View):  # height 2
    date = view(box('Pick a date', mode='date', value='2021-10-10', min='2019-01-01'))
    view(f'You picked {date}.')


# ## Set max date
# Set `max=` to specify a maximum date.
def date_max(view: View):  # height 2
    date = view(box('Pick a date', mode='date', value='2021-10-10', max='2022-12-31'))
    view(f'You picked {date}.')


# ## Combine min and max date
# Set both `min=` and `max=` to restrict selection between two dates.
def date_min_max(view: View):  # height 2
    date = view(box('Pick a date', mode='date', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
    view(f'You picked {date}.')


# ## Set range
# Set `range=` to a `(min, max)` tuple to restrict selection between two dates.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def date_range(view: View):  # height 2
    date = view(box('Pick a date', mode='date', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    view(f'You picked {date}.')


# ## Mark as required
# Set `required=True` to indicate that input is required.
def date_required(view: View):  # height 2
    date = view(box('Pick a date', mode='date', required=True))
    view(f'You picked {date}.')
