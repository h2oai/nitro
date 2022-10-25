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


# # Graphics
# Draw microcharts, sparklines, and other data graphics.

# ## Line Y
def graphics_line_y(view: View):  # height 3
    view(
        box(mode='g line-y', style='h-8', data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5]),
    )


# ## Area Y
def graphics_area_y(view: View):  # height 3
    view(
        box(mode='g area-y', style='h-8', data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5]),
    )


