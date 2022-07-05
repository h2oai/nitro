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


# # Banner
# Use banners to show errors, warnings, or important information related to an operation.

# ## Basic
# Set `mode=` to `'info'`, `'success'`, `'warning'`, `'critical'`, `'blocked'` or `'error'`  to show a banner.
def banner_basic(view: View):  # height 4
    view(
        box('This server is powered by a lemon and two electrodes.', mode='info'),
        box("The optimizer has been optimized!", mode='success'),
        box('It is pitch black. You are likely to be eaten by a grue.', mode='warning'),
        box('Thermal levels critical. Please wait while we consult the manual.', mode='critical'),
        box('Operation blocked. We are testing your patience.', mode='blocked'),
        box('Operation failed. Something is burning.', mode='error'),
    )
