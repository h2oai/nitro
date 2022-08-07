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

# ## Overview
# By default, `view()` overwrites all boxes displayed by the previous `view()`.
# However, you can also make `view()` selectively  append, update, insert or remove boxes.
#
# The following example uses `insert=` or `remove=` with `before=`, `at=` or `after=`
# to edit the view.
def edit_update(view: View):  # height 5
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    amber = 'p-2 rounded border text-amber-500 border-amber-500 bg-amber-100'
    red = 'p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100'
    green = 'p-2 rounded border text-green-500 border-green-500 bg-green-100'

    # Show some boxes:
    view(
        box('Blue 1', style=blue),
        box('Amber', style=amber, name='amber'),
        box('Blue 2', style=blue),
    )

    # Append a box:
    view(box('Appended', style=red), insert=True)

    # Insert a box before `amber`:
    view(box('Inserted', style=green), insert=True, before='amber')

    # Overwrite two boxes with three boxes after `amber`:
    view(
        box('Overwritten 1', style=green),
        box('Overwritten 2', style=green),
        box('Overwritten 3', style=green),
        after='amber',
    )

    # Remove everything before `amber`:
    view(remove=True, before='amber')


# ## Update at
# Set `at=` to overwrite boxes starting at an existing box.
def edit_update_at(view: View):  # height 3
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    red = 'p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100'
    green = 'p-2 rounded border text-green-500 border-green-500 bg-green-100'
    view(
        box('Blue', style=blue),
        box('Red 1', style=red, name='red1'),
        box('Red 2', style=red),
    )
    view(
        box('Green 1', style=green),
        box('Green 2', style=green),
        box('Green 3', style=green),
        at='red1',
    )


# ## Update before
# Set `before=` to overwrite boxes before an existing box.
def edit_update_before(view: View):  # height 4
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    amber = 'p-2 rounded border text-amber-500 border-amber-500 bg-amber-100'
    red = 'p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100'
    green = 'p-2 rounded border text-green-500 border-green-500 bg-green-100'
    view(
        box('Red', style=red),
        box('Amber', style=amber, name='amber'),
        box('Blue', style=blue),
    )
    view(
        box('Green 1', style=green),
        box('Green 2', style=green),
        box('Green 3', style=green),
        before='amber',
    )


# ## Update after
# Set `after=` to overwrite boxes after an existing box.
def edit_update_after(view: View):  # height 4
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    amber = 'p-2 rounded border text-amber-500 border-amber-500 bg-amber-100'
    red = 'p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100'
    green = 'p-2 rounded border text-green-500 border-green-500 bg-green-100'
    view(
        box('Blue', style=blue),
        box('Amber', style=amber, name='amber'),
        box('Red', style=red),
    )
    view(
        box('Green 1', style=green),
        box('Green 2', style=green),
        box('Green 3', style=green),
        after='amber',
    )


# ## Update inside
# Set `inside=` to overwrite boxes inside an existing box.
def edit_update_inside(view: View):  # height 4
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    amber = 'p-2 rounded border text-amber-500 border-amber-500 bg-amber-100'
    red = 'p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100'
    green = 'p-2 rounded border text-green-500 border-green-500 bg-green-100'
    view(
        box('Blue 1', style=blue),
        col(
            box('Red 1', style=red),
            box('Red 2', style=red),
            box('Red 3', style=red),
            style=amber,
            name='amber'
        ),
        box('Blue 2', style=blue),
    )
    view(
        box('Green 1', style=green),
        box('Green 2', style=green),
        box('Green 3', style=green),
        inside='amber',
    )


# ## Insert
# Set `insert=True` to insert boxes into an existing view.
#
# By default, new boxes are appended to the bottom of the view.
def edit_insert(view: View):  # height 5
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    green = 'p-2 rounded border text-green-500 border-green-500 bg-green-100'
    view(
        box('Blue 1', style=blue),
        box('Blue 2', style=blue),
        box('Blue 3', style=blue),
    )
    view(
        box('Green 1', style=green),
        box('Green 2', style=green),
        box('Green 3', style=green),
        insert=True,
    )


# ## Insert before
# Set `insert=True` with `before=` to insert boxes before an existing box.
def edit_insert_before(view: View):  # height 5
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    amber = 'p-2 rounded border text-amber-500 border-amber-500 bg-amber-100'
    green = 'p-2 rounded border text-green-500 border-green-500 bg-green-100'
    view(
        box('Blue 1', style=blue),
        box('Amber', style=amber, name='amber'),
        box('Blue 2', style=blue),
    )
    view(
        box('Green 1', style=green),
        box('Green 2', style=green),
        box('Green 3', style=green),
        insert=True, before='amber',
    )


# ## Insert at
# Setting `at=` has the same effect as `before=` when `Insert=True`.
def edit_insert_at(view: View):  # height 5
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    amber = 'p-2 rounded border text-amber-500 border-amber-500 bg-amber-100'
    green = 'p-2 rounded border text-green-500 border-green-500 bg-green-100'
    view(
        box('Blue 1', style=blue),
        box('Amber', style=amber, name='amber'),
        box('Blue 2', style=blue),
    )
    view(
        box('Green 1', style=green),
        box('Green 2', style=green),
        box('Green 3', style=green),
        insert=True, at='amber',
    )


# ## Insert after
# Set `insert=True` with `after=` to insert boxes after an existing box.
def edit_insert_after(view: View):  # height 4
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    amber = 'p-2 rounded border text-amber-500 border-amber-500 bg-amber-100'
    green = 'p-2 rounded border text-green-500 border-green-500 bg-green-100'
    view(
        box('Blue 1', style=blue),
        box('Amber', style=amber, name='amber'),
        box('Blue 2', style=blue),
    )
    view(
        box('Green 1', style=green),
        box('Green 2', style=green),
        box('Green 3', style=green),
        insert=True, after='amber',
    )


# ## Insert inside
# Set `insert=True` with `inside=` to insert boxes inside an existing box.
def edit_insert_inside(view: View):  # height 5
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    amber = 'p-2 rounded border text-amber-500 border-amber-500 bg-amber-100'
    green = 'p-2 rounded border text-green-500 border-green-500 bg-green-100'
    view(
        box('Blue 1', style=blue),
        col(
            box('Blue 2', style=blue),
            box('Blue 3', style=blue),
            style=amber,
            name='amber',
        ),
        box('Blue 4', style=blue),
    )
    view(
        box('Green 1', style=green),
        box('Green 2', style=green),
        insert=True, inside='amber',
    )


# ## Remove at
# Set `remove=True` with `at=` to remove an existing box.
def edit_remove_at(view: View):  # height 4
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    red = 'p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100'
    view(
        box('Blue 1', style=blue),
        box('Blue 2', style=blue),
        box('Red', style=red, name='red'),
        box('Blue 3', style=blue),
        box('Blue 4', style=blue),
    )
    view(remove=True, at='red')


# ## Remove before
# Set `remove=True` with `before=` to remove boxes before an existing box.
def edit_remove_before(view: View):  # height 4
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    amber = 'p-2 rounded border text-amber-500 border-amber-500 bg-amber-100'
    red = 'p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100'
    view(
        box('Red 1', style=red),
        box('Red 2', style=red),
        box('Amber', style=amber, name='amber'),
        box('Blue 1', style=blue),
        box('Blue 2', style=blue),
    )
    view(remove=True, before='amber')


# ## Remove after
# Set `remove=True` with `after=` to remove boxes after an existing box.
def edit_remove_after(view: View):  # height 4
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    amber = 'p-2 rounded border text-amber-500 border-amber-500 bg-amber-100'
    red = 'p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100'
    view(
        box('Blue 1', style=blue),
        box('Blue 2', style=blue),
        box('Amber', style=amber, name='amber'),
        box('Red 1', style=red),
        box('Red 2', style=red),
    )
    view(remove=True, after='amber')


# ## Remove inside
# Set `remove=True` with `inside=` to remove boxes inside an existing box.
def edit_remove_inside(view: View):  # height 5
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    amber = 'p-2 rounded border text-amber-500 border-amber-500 bg-amber-100'
    red = 'p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100'
    green = 'p-2 rounded border text-green-500 border-green-500 bg-green-100'
    view(
        box('Blue 1', style=blue),
        box('Blue 2', style=blue),
        col(
            box('Red 1', style=red),
            box('Red 2', style=red),
            box('Red 3', style=red),
            style=amber,
            name='amber'
        ),
        box('Blue 2', style=blue),
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
    blue = 'p-2 rounded border text-sky-500 border-sky-500 bg-sky-100'
    amber = 'p-2 rounded border text-amber-500 border-amber-500 bg-amber-100'
    red = 'p-2 rounded border border-dashed text-red-500 border-red-500 bg-red-100'
    green = 'p-2 rounded border text-green-500 border-green-500 bg-green-100'
    # Show a 3x3 grid
    view(
        box(
            col(
                box('Blue 1', style=blue),
                box('Blue 2', style=blue),
                box('Blue 3', style=blue),
                style=blue,
            ),
            col(
                box('Blue 4', style=blue),
                box('Amber', style=amber, name='amber'),
                box('Red', style=red),
                style=amber,
                name='col2',
            ),
            col(
                box('Blue 5', style=blue),
                box('Blue 6', style=blue),
                box('Blue 7', style=blue),
                style=blue,
            ),
            style='grid grid-cols-3 gap-2'
        ),
    )

    # Insert 2 boxes before `amber` inside `col2`.
    view(
        box('Green 1', style=green),
        box('Green 2', style=green),
        insert=True, before='col2 amber',
    )

    # Overwrite everything after `indigo` inside `col2`.
    view(
        box('Green 3', style=green),
        box('Green 4', style=green),
        after='col2 amber',
    )

    # Remove 'indigo'.
    view(remove=True, at='lime indigo')
