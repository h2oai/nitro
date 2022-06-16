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


# # Toggle

# ## Basic
# Set `mode='toggle'` to show a toggle.
#
# A toggle represents a physical switch that allows someone to choose between two mutually exclusive options.
# For example, “On/Off”, “Show/Hide”. Choosing an option should produce an immediate result.
#
# Note that unlike a checkbox, a toggle returns its value immediately, much like a button.
# This lets you handle the changed value immediately.
# To keep the toggle displayed until the user is done, call `view()` inside a `while` loop.
def toggle_basic(view: View):  # height 4
    glazed, sprinkles, hot, done = True, False, False, False
    while not done:
        glazed, sprinkles, hot, done = view(
            '### Customize my donut!',
            box('Make it glazed', mode='toggle', value=glazed),
            box('Add sprinkles', mode='toggle', value=sprinkles),
            box('Make it hot', mode='toggle', value=hot),
            box(['Place order'])
        )
    view(f'''
    You want your donut {"glazed" if glazed else "frosted"}, 
    {"with" if sprinkles else "without"} sprinkles, 
    and {"hot" if hot else "warm"}!
    ''')
