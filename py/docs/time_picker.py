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


# # Time Picker

# ## Basic
# Set `mode='time'` to show a time picker.
def time_basic(view: View):
    time = view(box('Set alarm for:', mode='time', value='3:04PM'))
    view(f'Alarm set for {time}.')


# ## With seconds
# Include seconds in the `value` to show a seconds component.
def time_seconds(view: View):
    time = view(box('Set alarm for:', mode='time', value='3:04:05PM'))
    view(f'Alarm set for {time}.')


# ## Hour only
# Exclude minutes and seconds from the `value` to show only the hour component.
def time_hour(view: View):
    time = view(box('Set alarm for:', mode='time', value='3PM'))
    view(f'Alarm set for {time}.')


# ## 24-hour clock
# Exclude `AM` or `PM` from the `value` to accept input in military time.
def time_24(view: View):
    time = view(box('Set alarm for:', mode='time', value='15:04'))
    view(f'Alarm set for {time}.')


# ## 24-hour clock, with seconds
# Include seconds in the `value` to show a seconds component.
def time_24_seconds(view: View):
    time = view(box('Set alarm for:', mode='time', value='15:04:05'))
    view(f'Alarm set for {time}.')


# ## 24-hour clock, hour only
# Exclude minutes and seconds from the `value` to show only the hour component.
def time_24_hour(view: View):
    time = view(box('Set alarm for:', mode='time', value='15'))
    view(f'Alarm set for {time}.')
