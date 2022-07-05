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


# # Progress Bar
# Use progress bars to show the completion status of long-running operations.

# ## Basic
# Set `mode='progress'` to show a progress bar.
def progress_bar_basic(view: View):  # height 2
    view(box('Swapping time and space...', mode='progress'))


# ## Set caption
# Set `caption=` to show a caption below the bar
def progress_bar_caption(view: View):  # height 2
    view(box(
        'Swapping time and space',
        mode='progress',
        caption='Spinning violently around the y-axis...',
    ))


# ## Set completion
# Set `value=` to a number between `0` and `1` to show a completion status.
def progress_bar_value(view: View):  # height 2
    view(box(
        'Swapping time and space',
        mode='progress',
        caption='Spinning violently around the y-axis...',
        value=0.75
    ))
