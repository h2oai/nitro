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
import datetime
import h2o_nitro.fake as fake


# # Format Dates
# Language-sensitive date, time, and relative time formatting.

# ## Basic
# Set the `date` style to format dates.
#
# Note that dates must be ISO 8601 formatted, with time zone information.
def format_date_basic(view: View):  # height 4
    now = datetime.datetime.now().astimezone().isoformat()
    view(
        box('=ISO: {now}', data=dict(now=now)),  # Raw date string (not formatted)
        box('=Active: {now date}', data=dict(now=now)),  # Active locale
        box('=US: {now date}', data=dict(now=now), locale='en-US'),
        box('=Germany: {now date}', data=dict(now=now), locale='de-DE'),
        box('=Egypt: {now date}', data=dict(now=now), locale='ar-EG'),
        box('=India: {now date}', data=dict(now=now), locale='en-IN'),
        box('=UK: {now date}', data=dict(now=now), locale='en-GB'),
    )


# ## Time
# Set the `time` style to format time.
def format_date_time(view: View):  # height 4
    now = datetime.datetime.now().astimezone().isoformat()
    view(
        box('=ISO: {now}', data=dict(now=now)),  # Raw date string (not formatted)
        box('=Active: {now time}', data=dict(now=now)),  # Active locale
        box('=US: {now time}', data=dict(now=now), locale='en-US'),
        box('=Germany: {now time}', data=dict(now=now), locale='de-DE'),
        box('=Egypt: {now time}', data=dict(now=now), locale='ar-EG'),
        box('=India: {now time}', data=dict(now=now), locale='en-IN'),
        box('=UK: {now time}', data=dict(now=now), locale='en-GB'),
    )


# ## Date and time
# Set both `date` and `time` styles to format date and time.
def format_date_datetime(view: View):  # height 4
    now = datetime.datetime.now().astimezone().isoformat()
    view(
        box('=ISO: {now}', data=dict(now=now)),  # Raw date string (not formatted)
        box('=Active: {now date time}', data=dict(now=now)),  # Active locale
        box('=US: {now date time}', data=dict(now=now), locale='en-US'),
        box('=Germany: {now date time}', data=dict(now=now), locale='de-DE'),
        box('=Egypt: {now date time}', data=dict(now=now), locale='ar-EG'),
        box('=India: {now date time}', data=dict(now=now), locale='en-IN'),
        box('=UK: {now date time}', data=dict(now=now), locale='en-GB'),
    )


# ## Date style
# Add one of `date-xl` (extra long), `date-l` (long), `date-m` (medium), or `date-s` (short) styles
# for additional control.
def format_date_length(view: View):  # height 6
    now = datetime.datetime.now().astimezone().isoformat()
    view(
        box('=ISO: {now}', data=dict(now=now)),  # Raw date string (not formatted)
        '## US',
        box('=Full: {now date-xl}', data=dict(now=now), locale='en-US'),
        box('=Long: {now date-l}', data=dict(now=now), locale='en-US'),
        box('=Medium: {now date-m}', data=dict(now=now), locale='en-US'),
        box('=Short: {now date-s}', data=dict(now=now), locale='en-US'),
        '## UK',
        box('=Full: {now date-xl}', data=dict(now=now), locale='en-GB'),
        box('=Long: {now date-l}', data=dict(now=now), locale='en-GB'),
        box('=Medium: {now date-m}', data=dict(now=now), locale='en-GB'),
        box('=Short: {now date-s}', data=dict(now=now), locale='en-GB'),
    )


# ## Time style
# Add one of `time-xl` (extra long), `time-l` (long), `time-m` (medium), or `time-s` (short) styles
# for additional control.
def format_date_time_length(view: View):  # height 6
    now = datetime.datetime.now().astimezone().isoformat()
    view(
        box('=ISO: {now}', data=dict(now=now)),  # Raw date string (not formatted)
        '## US',
        box('=Full: {now time-xl}', data=dict(now=now), locale='en-US'),
        box('=Long: {now time-l}', data=dict(now=now), locale='en-US'),
        box('=Medium: {now time-m}', data=dict(now=now), locale='en-US'),
        box('=Short: {now time-s}', data=dict(now=now), locale='en-US'),
        '## UK',
        box('=Full: {now time-xl}', data=dict(now=now), locale='en-GB'),
        box('=Long: {now time-l}', data=dict(now=now), locale='en-GB'),
        box('=Medium: {now time-m}', data=dict(now=now), locale='en-GB'),
        box('=Short: {now time-s}', data=dict(now=now), locale='en-GB'),
    )

