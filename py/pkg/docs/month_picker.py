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
# Use a month picker to pick a month in a given range.

# ## Basic
# Set `mode='month'` to show a month picker.
def month_basic(view: View):  # height 4
    month = view(box('Pick a month', mode='month'))
    view(f'You picked {month}.')


# ## Set initial month
# Set `value=` to pre-select a month.
#
# Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
# Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.
def month_value(view: View):  # height 4
    month = view(box('Pick a month', mode='month', value='2021-10-10'))
    view(f'You picked {month}.')


# ## Set min date
# Set `min=` to specify a minimum date.
def month_min(view: View):  # height 4
    month = view(box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01'))
    view(f'You picked {month}.')


# ## Set max date
# Set `max=` to specify a maximum date.
def month_max(view: View):  # height 4
    month = view(box('Pick a month', mode='month', value='2021-10-10', max='2022-12-31'))
    view(f'You picked {month}.')


# ## Combine min and max dates
# Set both `min=` and `max=` to restrict selection between two dates.
def month_min_max(view: View):  # height 4
    month = view(box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
    view(f'You picked {month}.')


# ## Set range
# Set `range=` to a `(min, max)` tuple to restrict selection between two dates.
#
# This is a shorthand notation for setting `min=` and `max=` individually.
def month_range(view: View):  # height 4
    month = view(box('Pick a month', mode='month', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
    view(f'You picked {month}.')


# ## Handle changes immediately
# Add `live` to `mode` to handle changes immediately.
def month_live(view: View):  # height 4
    month = '2021-10-10'
    while True:
        month = view(
            box('Pick a month', mode='live month', value=month),
            f'You picked {month} (UTC).'
        )
