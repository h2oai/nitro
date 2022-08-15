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


from h2o_nitro import View, box, row, col, option, lorem, Theme


# # Editing
# Make changes to content already displayed on a page.

# ## Basics
# By default, `view()` overwrites all boxes displayed by the previous `view()`.
# It's also possible to selectively modify the previous view instead of overwriting it entirely.
#
# The following example uses `view()`, `view.add()` and `view.clear()` to modify the current view.
#
# The `at` argument indicates where to add, overwrite or clear boxes.
#
# - `foo`: from box `foo` (or at box `foo`).
# - `:foo`: before box `foo`.
# - `foo:`: after box `foo`.
# - `foo *`: inside box `foo`.
# - `foo bar`: from box `foo`'s child box `bar` (or at box `foo`'s child box `bar`).
# - `foo :bar`: before box `foo`'s child box `bar`.
# - `foo bar:`: after box `foo`'s child box `bar`.
# - `foo bar *`: inside box `foo`'s child box `bar`.
def edit_overwrite(view: View):  # height 5
    blue, amber, red, green = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                               ['sky', 'amber', 'red', 'green']]

    # Show some boxes:
    view(
        blue('Blue 1'),
        amber('Amber', name='amber'),
        blue('Blue 2'),
    )

    # Add a box:
    view.add(red('Appended'))

    # Add a box before `amber`:
    view.add(green('Added'), at=':amber')

    # Overwrite two boxes with three other boxes after `amber`:
    view(
        green('Overwritten 1'),
        green('Overwritten 2'),
        green('Overwritten 3'),
        at='amber:',
    )

    # Clear everything before `amber`:
    view.clear(at=':amber')


# ## Overwrite
# Set `at='name'` to overwrite boxes starting at an existing box.
def edit_overwrite_at(view: View):  # height 3
    blue, red, green = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                        ['sky', 'red', 'green']]
    view(
        blue('Blue'),
        red('Red 1', name='red1'),
        red('Red 2'),
    )
    view(
        green('Green 1'),
        green('Green 2'),
        green('Green 3'),
        at='red1',
    )


# ## Overwrite before
# Set `at=':name'` to overwrite boxes before an existing box.
def edit_overwrite_before(view: View):  # height 4
    blue, amber, red, green = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                               ['sky', 'amber', 'red', 'green']]
    view(
        red('Red'),
        amber('Amber', name='amber'),
        blue('Blue'),
    )
    view(
        green('Green 1'),
        green('Green 2'),
        green('Green 3'),
        at=':amber',
    )


# ## Overwrite after
# Set `at='name:'` to overwrite boxes after an existing box.
def edit_overwrite_after(view: View):  # height 4
    blue, amber, red, green = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                               ['sky', 'amber', 'red', 'green']]
    view(
        blue('Blue'),
        amber('Amber', name='amber'),
        red('Red'),
    )
    view(
        green('Green 1'),
        green('Green 2'),
        green('Green 3'),
        at='amber:',
    )


# ## Overwrite inside
# Set `at='name *'` to overwrite boxes inside an existing box.
def edit_overwrite_inside(view: View):  # height 4
    blue, red, green = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                        ['sky', 'red', 'green']]
    view(
        blue('Blue 1'),
        col(
            red('Red 1'),
            red('Red 2'),
            red('Red 3'),
            style='p-2 bg-stripes-amber',
            name='amber'
        ),
        blue('Blue 2'),
    )
    view(
        green('Green 1'),
        green('Green 2'),
        green('Green 3'),
        at='amber *',
    )


# ## Add
# Call `view.add()` to add boxes to the existing view.
#
# By default, new boxes are appended to the bottom of the view.
def edit_add(view: View):  # height 5
    blue, green = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                   ['sky', 'green']]
    view(
        blue('Blue 1'),
        blue('Blue 2'),
        blue('Blue 3'),
    )
    view.add(
        green('Green 1'),
        green('Green 2'),
        green('Green 3'),
    )


# ## Add before
# Set `at=':name'` to add boxes before an existing box.
def edit_add_before(view: View):  # height 5
    blue, amber, green = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                          ['sky', 'amber', 'green']]
    view(
        blue('Blue 1'),
        amber('Amber', name='amber'),
        blue('Blue 2'),
    )
    view.add(
        green('Green 1'),
        green('Green 2'),
        green('Green 3'),
        at=':amber',
    )


# ## Add at
# Setting `at='name'` has the same effect as `at=':name'` when calling `view.add()`,
# i.e. "add at" is the same as "add before".
def edit_add_at(view: View):  # height 5
    blue, amber, green = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                          ['sky', 'amber', 'green']]
    view(
        blue('Blue 1'),
        amber('Amber', name='amber'),
        blue('Blue 2'),
    )
    view.add(
        green('Green 1'),
        green('Green 2'),
        green('Green 3'),
        at='amber',
    )


# ## Add after
# Set `at='name:'` to add boxes after an existing box.
def edit_add_after(view: View):  # height 4
    blue, amber, green = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                          ['sky', 'amber', 'green']]
    view(
        blue('Blue 1'),
        amber('Amber', name='amber'),
        blue('Blue 2'),
    )
    view.add(
        green('Green 1'),
        green('Green 2'),
        green('Green 3'),
        at='amber:',
    )


# ## Add inside
# Set `at='name *'` to add boxes inside an existing box.
def edit_add_inside(view: View):  # height 5
    blue, green = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                   ['sky', 'green']]
    view(
        blue('Blue 1'),
        col(
            blue('Blue 2'),
            blue('Blue 3'),
            style='p-2 bg-stripes-amber',
            name='amber',
        ),
        blue('Blue 4'),
    )
    view.add(
        green('Green 1'),
        green('Green 2'),
        at='amber *',
    )


# ## Clear
# Call `view.clear() to remove a box.
def edit_clear_at(view: View):  # height 4
    blue, red = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                 ['sky', 'red']]
    view(
        blue('Blue 1'),
        blue('Blue 2'),
        red('Red', name='red'),
        blue('Blue 3'),
        blue('Blue 4'),
    )
    view.clear(at='red')


# ## Clear before
# Set `at=':name'` to clear everything before a box.
def edit_clear_before(view: View):  # height 4
    blue, amber, red = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                        ['sky', 'amber', 'red']]
    view(
        red('Red 1'),
        red('Red 2'),
        amber('Amber', name='amber'),
        blue('Blue 1'),
        blue('Blue 2'),
    )
    view.clear(at=':amber')


# ## Clear after
# Set `at='name:'` to clear everything after a box.
def edit_clear_after(view: View):  # height 4
    blue, amber, red = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                        ['sky', 'amber', 'red']]
    view(
        blue('Blue 1'),
        blue('Blue 2'),
        amber('Amber', name='amber'),
        red('Red 1'),
        red('Red 2'),
    )
    view.clear(at='amber:')


# ## Clear inside
# Set `at='name *'` to clear everything inside a box.
def edit_clear_inside(view: View):  # height 5
    blue, amber, red, green = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                               ['sky', 'amber', 'red', 'green']]
    view(
        blue('Blue 1'),
        blue('Blue 2'),
        col(
            red('Red 1'),
            red('Red 2'),
            red('Red 3'),
            style='p-2 bg-stripes-amber',
            name='amber'
        ),
        blue('Blue 2'),
    )
    view.clear(at='amber *')


# ## Selecting nested boxes
# Set `at=` to space-separated names to select nested items.
#
# - `foo` refers to the box named `foo`.
# - `foo bar` refers to the box named `bar` inside the box named `foo`.
# - `foo bar baz` refers to the box named `baz` inside the box named `bar` inside the box named `foo`.
# - ...and so on.
def edit_add_before_nested(view: View):  # height 5
    blue, amber, red, green = [box() / f'p-2 rounded border text-{c}-500 border-{c}-500 bg-{c}-100' for c in
                               ['sky', 'amber', 'red', 'green']]
    # Show a 3x3 grid
    view(
        box(
            col(
                blue('Blue 1'),
                blue('Blue 2'),
                blue('Blue 3'),
                style='p-2 bg-stripes-blue',
            ),
            col(
                blue('Blue 4'),
                amber('Amber', name='amber'),
                red('Red'),
                style='p-2 bg-stripes-lime',
                name='lime',
            ),
            col(
                blue('Blue 5'),
                blue('Blue 6'),
                blue('Blue 7'),
                style='p-2 bg-stripes-blue',
            ),
            style='grid grid-cols-3 gap-2'
        ),
    )

    # Add 2 boxes before `amber` inside `lime`.
    view.add(
        green('Green 1'),
        green('Green 2'),
        at='lime :amber',
    )

    # Overwrite everything after `amber` inside `lime`.
    view(
        green('Green 3'),
        green('Green 4'),
        at='lime amber:',
    )

    # Clear 'amber'.
    view.clear(at='lime amber')
