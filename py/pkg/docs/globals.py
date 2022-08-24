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


# # Globals
# Configure top-level menu, navigation and hotkeys.

# ## Hotkeys
# Set `hotkeys=` to configure keyboard shortcuts.
#
# Examples:
# - `option(cut, 'x')` calls the function `cut()` when `x` is pressed.
# - `option(cut, 'ctrl+x')` calls the function `cut()` when `control` and `x` are pressed together.
# - `option(cut, 'ctrl+shift+x')` calls the function `cut()` when `control`, `shift` and `x` are pressed together.
# - `option(cut, 'ctrl+x, command+x')` calls the function `cut()` when either `ctrl+x` or `command+x` are pressed.
#
# Supported modifiers: `shift`, `option`, `alt`, `ctrl`, `control`, `command`.
#
# Supported special keys: `backspace`, `tab`, `clear`, `enter`, `return`, `esc`, `escape`, `space`, `up`, `down`,
# `left`, `right`, `home`, `end`, `pageup`, `pagedown`, `del`, `delete`, `f1` - `f19`, `num_0` - `num_9`,
# `num_multiply`, `num_add`, `num_enter`, `num_subtract`, `num_decimal`, `num_divide`.
def hotkeys_basic_noop(view: View):  # height 3
    # Hotkey handler for Cut (ctrl+x)
    def cut(view: View):
        print('Cut!')

    # Hotkey handler for Copy (ctrl+c)
    def copy(view: View):
        print('Copy!')

    # Hotkey handler for Paste (ctrl+v)
    def paste(view: View):
        print('Paste!')

    # App entry point
    def main(view: View):
        pass

    # Pass hotkeys= to register hotkey handlers
    nitro = View(main, title='My App', caption='v1.0', hotkeys=[
        option(cut, 'ctrl+x'),
        option(copy, 'ctrl+c'),
        option(paste, 'ctrl+v'),
    ])

    view()
