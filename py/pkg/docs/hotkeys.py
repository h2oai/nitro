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


# # Hotkeys
# Assign keyboard shortcuts to actions.

# ## Tap
# Set `hotkey=` to assign a keyboard shortcut to a `tap` `input` box.
#
# Examples:
# - `hotkey='x'`: `x` is pressed.
# - `hotkey='ctrl+x'`:  `control` and `x` are pressed together.
# - `hotkey='ctrl+shift+x'`: `control`, `shift` and `x` are pressed together.
# - `hotkey='ctrl+x, command+x'`: either `ctrl+x` or `command+x` are pressed.
#
# Supported modifiers: `shift`, `option`, `alt`, `ctrl`, `control`, `command`.
#
# Supported special keys: `backspace`, `tab`, `clear`, `enter`, `return`, `esc`, `escape`, `space`, `up`, `down`,
# `left`, `right`, `home`, `end`, `pageup`, `pagedown`, `del`, `delete`, `f1` - `f19`, `num_0` - `num_9`,
# `num_multiply`, `num_add`, `num_enter`, `num_subtract`, `num_decimal`, `num_divide`.
def hotkey_tap(view: View):  # height 2
    style = 'text-white rounded-full px-5 py-2.5 text-center mr-2 mb-2 '
    color = view(
        'This is your last chance. After this, there is no turning back.',
        row(
            box(
                'Press Alt+b to take the blue pill',
                mode='tap', value='blue', hotkey='alt+b'
            ) / (style + 'bg-blue-700 hover:bg-blue-800'),
            box(
                'Press Alt+r to take the red pill',
                mode='tap', value='red', hotkey='alt+r'
            ) / (style + 'bg-red-700 hover:bg-red-800'),
            mode='input',
            ),
    )
    view(f'You took the {color} pill!')
