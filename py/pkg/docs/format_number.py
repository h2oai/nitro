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
def format_number_basic(view: View):  # height 4
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


# ## Percent
# Set the `pct` style to format numbers as percentages.
def format_number_percent(view: View):  # height 2
    view(
        box('=Percent: {donuts pct}', data=dict(donuts=0.6789))
    )


# ## Scientific
# Set the `sci` style to format numbers using scientific notation.
def format_number_scientific(view: View):  # height 2
    view(
        box('=Donuts: {donuts sci}', data=dict(donuts=123456.789))
    )


# ## Engineering
# Set the `sci` style to format numbers using engineering notation.
def format_number_engineering(view: View):  # height 2
    view(
        box('=Donuts: {donuts eng}', data=dict(donuts=123456.789))
    )


# ## Compact
# Set the `num-s` (short) or `num-xs` (extra short) style to format numbers using a compact notation.
def format_number_compact(view: View):  # height 4
    view(
        '## English',
        box('=Normal: {donuts num}', data=dict(donuts=1234567.89)),
        box('=Short: {donuts num-s}', data=dict(donuts=1234567.89)),
        box('=Extra Short: {donuts num-xs}', data=dict(donuts=1234567.89)),
        '## German',
        box('=Normal: {donuts num}', data=dict(donuts=1234567.89), locale='de'),
        box('=Short: {donuts num-s}', data=dict(donuts=1234567.89), locale='de'),
        box('=Extra Short: {donuts num-xs}', data=dict(donuts=1234567.89), locale='de'),
    )


# ## Currency
# Set the `cur-*` style to format currencies.
#
# Possible values are the ISO 4217 currency codes, such as `cur-USD` for the US dollar, `cur-EUR` for the euro,
# or `cur-CNY` for the Chinese RMB
# — see the [Current currency & funds code list](https://www.six-group.com/en/products-services/financial-information/data-standards.html#scrollTo=currency-codes).
#
# Add one of `cur-l` (long), `cur-m` (medium), `cur-s` (short), `cur-xs` (extra short) styles for additional control.
#
def format_number_currency(view: View):  # height 5
    view(
        '## Currencies',
        box('={price cur-USD}', data=dict(price=123456.789)),
        box('={price cur-EUR}', data=dict(price=123456.789)),
        box('={price cur-RMB}', data=dict(price=123456.789)),
        '## Notation',
        box('={price cur-USD cur-l}', data=dict(price=123456.789)),
        box('={price cur-USD cur-m}', data=dict(price=123456.789)),
        box('={price cur-USD cur-s}', data=dict(price=123456.789)),
        box('={price cur-USD cur-xs}', data=dict(price=123456.789)),
    )


# ## Accounting
# Set the `acc` style to wrap the number with parentheses instead of prefixing a minus sign.
#
# Note that this feature is locale-sensitive, and might not make a difference in many locales.
def format_number_accounting(view: View):  # height 3
    view(
        box('=Positive: {price cur-USD acc}', data=dict(price=123456.789)),
        box('=Negative: {price cur-USD acc}', data=dict(price=-123456.789)),

        # Makes no difference in Germany:
        box('=Negative: {price cur-EUR acc}', data=dict(price=-123456.789), locale='de'),
    )

