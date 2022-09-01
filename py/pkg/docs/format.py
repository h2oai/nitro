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


# # Format
# Learn the basics of formatting and templates.

# ## Basic
# Combine template strings with `data=` to perform string interpolation.
#
# A _template string_ is any string that begins with a literal`=`.
def format_basic(view: View):  # height 2
    view(box('=You bought {count} {product}.', data=dict(count=42, product='donuts')))


# ## Nested data
# Use dot-notation to access nested data.
def format_nested(view: View):  # height 2
    view(box(
        '={greeting}, {name.first} {name.last}!.',
        data=dict(
            greeting='Hello',
            name=dict(
                first='Boaty',
                last='McBoatface',
            ),
        )
    ))


# ## Arrays
# Use 0-based integers to access arrays.
#
# This notation is more compact, but less readable.
def format_array(view: View):  # height 2
    view(box('={0}, {1} {2}!.', data=['Hello', 'Boaty', 'McBoatface']))


# ## Nested arrays
# Combine dot-notation with 0-based integers to access nested arrays.
def format_nested_array(view: View):  # height 2
    view(box(
        '={greeting}, {name.0} {name.1}!.',
        data=dict(greeting='Hello', name=['Boaty', 'McBoatface'])
    ))
