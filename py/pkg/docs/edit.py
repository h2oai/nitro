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


from h2o_nitro import View, box, row, col, part, option, lorem, Theme


# # Editing
# Make changes to content already displayed on a page.

# ## Overview
# By default, `view()` overwrites all boxes displayed by the previous `view()`.
# However, you can also make `view()` selectively  append, update, insert or remove boxes.
#
# The following example uses `insert=` or `remove=` with `before=`, `at=` or `after=`
# to edit the view.
def edit_update(view: View):  # height 5
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
    red = part('p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100')
    green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')

    # Show some boxes:
    view(
        blue('Blue 1'),
        amber('Amber', name='amber'),
        blue('Blue 2'),
    )

    # Append a box:
    view(red('Appended'), insert=True)

    # Insert a box before `amber`:
    view(green('Inserted'), insert=True, before='amber')

    # Overwrite two boxes with three boxes after `amber`:
    view(
        green('Overwritten 1'),
        green('Overwritten 2'),
        green('Overwritten 3'),
        after='amber',
    )

    # Remove everything before `amber`:
    view(remove=True, before='amber')


# ## Update at
# Set `at=` to overwrite boxes starting at an existing box.
def edit_update_at(view: View):  # height 3
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    red = part('p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100')
    green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
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


# ## Update before
# Set `before=` to overwrite boxes before an existing box.
def edit_update_before(view: View):  # height 4
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
    red = part('p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100')
    green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
    view(
        red('Red'),
        amber('Amber', name='amber'),
        blue('Blue'),
    )
    view(
        green('Green 1'),
        green('Green 2'),
        green('Green 3'),
        before='amber',
    )


# ## Update after
# Set `after=` to overwrite boxes after an existing box.
def edit_update_after(view: View):  # height 4
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
    red = part('p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100')
    green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
    view(
        blue('Blue'),
        amber('Amber', name='amber'),
        red('Red'),
    )
    view(
        green('Green 1'),
        green('Green 2'),
        green('Green 3'),
        after='amber',
    )


# ## Update inside
# Set `inside=` to overwrite boxes inside an existing box.
def edit_update_inside(view: View):  # height 4
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
    red = part('p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100')
    green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
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
        inside='amber',
    )


# ## Insert
# Set `insert=True` to insert boxes into an existing view.
#
# By default, new boxes are appended to the bottom of the view.
def edit_insert(view: View):  # height 5
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
    view(
        blue('Blue 1'),
        blue('Blue 2'),
        blue('Blue 3'),
    )
    view(
        green('Green 1'),
        green('Green 2'),
        green('Green 3'),
        insert=True,
    )


# ## Insert before
# Set `insert=True` with `before=` to insert boxes before an existing box.
def edit_insert_before(view: View):  # height 5
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
    green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
    view(
        blue('Blue 1'),
        amber('Amber', name='amber'),
        blue('Blue 2'),
    )
    view(
        green('Green 1'),
        green('Green 2'),
        green('Green 3'),
        insert=True, before='amber',
    )


# ## Insert at
# Setting `at=` has the same effect as `before=` when `Insert=True`.
def edit_insert_at(view: View):  # height 5
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
    green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
    view(
        blue('Blue 1'),
        amber('Amber', name='amber'),
        blue('Blue 2'),
    )
    view(
        green('Green 1'),
        green('Green 2'),
        green('Green 3'),
        insert=True, at='amber',
    )


# ## Insert after
# Set `insert=True` with `after=` to insert boxes after an existing box.
def edit_insert_after(view: View):  # height 4
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
    green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
    view(
        blue('Blue 1'),
        amber('Amber', name='amber'),
        blue('Blue 2'),
    )
    view(
        green('Green 1'),
        green('Green 2'),
        green('Green 3'),
        insert=True, after='amber',
    )


# ## Insert inside
# Set `insert=True` with `inside=` to insert boxes inside an existing box.
def edit_insert_inside(view: View):  # height 5
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
    green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
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
    view(
        green('Green 1'),
        green('Green 2'),
        insert=True, inside='amber',
    )


# ## Remove at
# Set `remove=True` with `at=` to remove an existing box.
def edit_remove_at(view: View):  # height 4
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    red = part('p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100')
    view(
        blue('Blue 1'),
        blue('Blue 2'),
        red('Red', name='red'),
        blue('Blue 3'),
        blue('Blue 4'),
    )
    view(remove=True, at='red')


# ## Remove before
# Set `remove=True` with `before=` to remove boxes before an existing box.
def edit_remove_before(view: View):  # height 4
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
    red = part('p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100')
    view(
        red('Red 1'),
        red('Red 2'),
        amber('Amber', name='amber'),
        blue('Blue 1'),
        blue('Blue 2'),
    )
    view(remove=True, before='amber')


# ## Remove after
# Set `remove=True` with `after=` to remove boxes after an existing box.
def edit_remove_after(view: View):  # height 4
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
    red = part('p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100')
    view(
        blue('Blue 1'),
        blue('Blue 2'),
        amber('Amber', name='amber'),
        red('Red 1'),
        red('Red 2'),
    )
    view(remove=True, after='amber')


# ## Remove inside
# Set `remove=True` with `inside=` to remove boxes inside an existing box.
def edit_remove_inside(view: View):  # height 5
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
    red = part('p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100')
    green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
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
    view(remove=True, inside='amber')


# ## Selecting nested boxes
# Set `at=`, `before=`, or `after=` to space-separated names to select nested items.
#
# - `before='foo'` means *before the box named `foo`*.
# - `before='foo bar'` means *before the box named `bar` inside the box named `foo`*.
# - `before='foo bar baz'` means *before the box named `baz` inside the box named `bar`, inside the box named `foo`*.
# - ...and so on.
def edit_insert_before_nested(view: View):  # height 5
    blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
    amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
    red = part('p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100')
    green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
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
                style='p-2 bg-stripes-amber',
                name='col2',
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

    # Insert 2 boxes before `amber` inside `col2`.
    view(
        green('Green 1'),
        green('Green 2'),
        insert=True, before='col2 amber',
    )

    # Overwrite everything after `indigo` inside `col2`.
    view(
        green('Green 3'),
        green('Green 4'),
        after='col2 amber',
    )

    # Remove 'indigo'.
    view(remove=True, at='lime indigo')
