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
import h2o_nitro.fake as fake


# # Format Numbers
# Language-sensitive number and currency formatting.


# ## Basic
# Set the `num` style to format numbers.
def format_number_basic(view: View):  # height 2
    view(
        # Format using active application-wide locale.
        box('=Active: {donuts num}', data=dict(donuts=123456.789)),

        # US English
        box('=US: {donuts num}', data=dict(donuts=123456.789), locale='en-US'),

        # Germany uses comma as decimal separator and period for thousands
        box('=Germany: {donuts num}', data=dict(donuts=123456.789), locale='de-DE'),

        # Arabic in most Arabic speaking countries uses real Arabic digits
        box('=Egypt: {donuts num}', data=dict(donuts=123456.789), locale='ar-EG'),

        # India uses thousands/lakh/crore separators.
        box('=India: {donuts num}', data=dict(donuts=123456.789), locale='en-IN'),

        # Use an alternate numbering system, e.g. Chinese decimal.
        box('=China: {donuts num}', data=dict(donuts=123456.789), locale='zh-Hans-CN-u-nu-hanidec'),

        # Use Balinese if available, else fallback to Indonesian.
        box('=Indonesia: {donuts num}', data=dict(donuts=123456.789), locale=('ban', 'id')),

    )
