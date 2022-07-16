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
    # Display some boxes:
    view(
        box('Blue 1', background='$blue', color='white'),
        box('Blue 2', background='$blue', color='white', name='blue2'),
        box('Blue 3', background='$blue', color='white'),
    )

    # Append a box:
    view(
        box('Appended', background='$lava', color='white'),
        insert=True,
    )

    # Insert a box before `blue2`:
    view(
        box('Inserted', background='$lava', color='white'),
        insert=True, before='blue2',
    )

    # Overwrite two boxes with three boxes after `blue2`:
    view(
        box('Overwritten 1', background='$lava', color='white'),
        box('Overwritten 2', background='$lava', color='white'),
        box('Overwritten 3', background='$lava', color='white'),
        after='blue2',
    )

    # Remove everything before `blue2`:
    view(remove=True, before='blue2')


# ## Update at
# Set `at=` to overwrite boxes starting at an existing box.
def edit_update_at(view: View):  # height 4
    view(
        box('Blue 1', background='$blue', color='white'),
        box('Indigo', name='indigo', background='$indigo', color='white'),
        box('Blue 2', background='$blue', color='white'),
    )
    view(
        box('Red 1', background='$lava', color='white'),
        box('Red 2', background='$lava', color='white'),
        box('Red 3', background='$lava', color='white'),
        at='indigo',
    )


# ## Update before
# Set `before=` to overwrite boxes before an existing box.
def edit_update_before(view: View):  # height 4
    view(
        box('Blue 1', background='$blue', color='white'),
        box('Indigo', name='indigo', background='$indigo', color='white'),
        box('Blue 2', background='$blue', color='white'),
    )
    view(
        box('Red 1', background='$lava', color='white'),
        box('Red 2', background='$lava', color='white'),
        box('Red 3', background='$lava', color='white'),
        before='indigo',
    )


# ## Update after
# Set `after=` to overwrite boxes after an existing box.
def edit_update_after(view: View):  # height 4
    view(
        box('Blue 1', background='$blue', color='white'),
        box('Indigo', name='indigo', background='$indigo', color='white'),
        box('Blue 2', background='$blue', color='white'),
    )
    view(
        box('Red 1', background='$lava', color='white'),
        box('Red 2', background='$lava', color='white'),
        box('Red 3', background='$lava', color='white'),
        after='indigo',
    )


# ## Update inside
# Set `inside=` to overwrite boxes inside an existing box.
def edit_update_inside(view: View):  # height 4
    view(
        box('Blue 1', background='$blue', color='white'),
        col(
            box('Indigo 1', background='$indigo', color='white'),
            box('Indigo 2', background='$indigo', color='white'),
            box('Indigo 3', background='$indigo', color='white'),
            name='indigo'
        ),
        box('Blue 2', background='$blue', color='white'),
    )
    view(
        box('Red 1', background='$lava', color='white'),
        box('Red 2', background='$lava', color='white'),
        box('Red 3', background='$lava', color='white'),
        inside='indigo',
    )


# ## Insert
# Set `insert=True` to insert boxes into an existing view.
#
# By default, new boxes are appended to the bottom of the view.
def edit_insert(view: View):  # height 5
    view(
        box('Blue 1', background='$blue', color='white'),
        box('Blue 2', background='$blue', color='white'),
        box('Blue 3', background='$blue', color='white'),
    )
    view(
        box('Red 1', background='$lava', color='white'),
        box('Red 2', background='$lava', color='white'),
        box('Red 3', background='$lava', color='white'),
        insert=True,
    )


# ## Insert before
# Set `insert=True` and `before=` to insert boxes before an existing box.
def edit_insert_before(view: View):  # height 5
    view(
        box('Blue 1', background='$blue', color='white'),
        box('Indigo', name='indigo', background='$indigo', color='white'),
        box('Blue 2', background='$blue', color='white'),
    )
    view(
        box('Red 1', background='$lava', color='white'),
        box('Red 2', background='$lava', color='white'),
        box('Red 3', background='$lava', color='white'),
        insert=True, before='indigo',
    )


# ## Insert at
# Setting `at=` has the same effect as `before=` when `Insert=True`.
def edit_insert_at(view: View):  # height 5
    view(
        box('Blue 1', background='$blue', color='white'),
        box('Indigo', name='indigo', background='$indigo', color='white'),
        box('Blue 2', background='$blue', color='white'),
    )
    view(
        box('Red 1', background='$lava', color='white'),
        box('Red 2', background='$lava', color='white'),
        box('Red 3', background='$lava', color='white'),
        insert=True, at='indigo',
    )


# ## Insert after
# Set `insert=True` and `after=` to insert boxes after an existing box.
def edit_insert_after(view: View):
    view(
        box('Blue 1', background='$blue', color='white'),
        box('Indigo', name='indigo', background='$indigo', color='white'),
        box('Blue 2', background='$blue', color='white'),
    )
    view(
        box('Red 1', background='$lava', color='white'),
        box('Red 2', background='$lava', color='white'),
        box('Red 3', background='$lava', color='white'),
        insert=True, after='indigo',
    )


# ## Insert inside
# Set `insert=True` and `inside=` to insert boxes inside an existing box.
def insert_update_inside(view: View):  # height 5
    view(
        box('Blue 1', background='$blue', color='white'),
        col(
            box('Indigo 1', background='$indigo', color='white'),
            box('Indigo 2', background='$indigo', color='white'),
            name='indigo'
        ),
        box('Blue 2', background='$blue', color='white'),
    )
    view(
        box('Red 1', background='$lava', color='white'),
        box('Red 2', background='$lava', color='white'),
        insert=True, inside='indigo',
    )


# ## Remove at
# Set `remove=True` and `at=` to remove an existing box.
def edit_remove_at(view: View):  # height 4
    view(
        box('Blue 1', background='$blue', color='white'),
        box('Blue 2', background='$blue', color='white'),
        box('Indigo', name='indigo', background='$indigo', color='white'),
        box('Blue 3', background='$blue', color='white'),
        box('Blue 4', background='$blue', color='white'),
    )
    view(remove=True, at='indigo')


# ## Remove before
# Set `remove=True` and `before=` to remove boxes before an existing box.
def edit_remove_before(view: View):  # height 4
    view(
        box('Blue 1', background='$blue', color='white'),
        box('Blue 2', background='$blue', color='white'),
        box('Indigo', name='indigo', background='$indigo', color='white'),
        box('Blue 3', background='$blue', color='white'),
        box('Blue 4', background='$blue', color='white'),
    )
    view(remove=True, before='indigo')


# ## Remove before
# Set `remove=True` and `after=` to remove boxes after an existing box.
def edit_remove_after(view: View):  # height 4
    view(
        box('Blue 1', background='$blue', color='white'),
        box('Blue 2', background='$blue', color='white'),
        box('Indigo', name='indigo', background='$indigo', color='white'),
        box('Blue 3', background='$blue', color='white'),
        box('Blue 4', background='$blue', color='white'),
    )
    view(remove=True, after='indigo')


# ## Remove inside
# Set `remove=True` and `inside=` to remove boxes inside an existing box.
def edit_remove_inside(view: View):  # height 4
    view(
        box('Blue 1', background='$blue', color='white'),
        col(
            box('Indigo 1', background='$indigo', color='white'),
            box('Indigo 2', background='$indigo', color='white'),
            box('Indigo 3', background='$indigo', color='white'),
            name='indigo'
        ),
        box('Blue 2', background='$blue', color='white'),
    )
    view(remove=True, inside='indigo')


# ## Selecting nested boxes
# Set `at=`, `before=`, or `after=` to space-separated names to select nested items.
#
# - `before='foo'` means *before the box named `foo`*.
# - `before='foo bar'` means *before the box named `bar` inside the box named `foo`*.
# - `before='foo bar baz'` means *before the box named `baz` inside the box named `bar`, inside the box named `foo`*.
# - ...and so on.
def edit_insert_before_nested(view: View):  # height 5
    # Show a 3x3 grid
    view(
        row(
            col(
                box('Yellow 1', background='$yellow', color='black'),
                box('Yellow 2', background='$yellow', color='black'),
                box('Yellow 3', background='$yellow', color='black'),
            ),
            col(
                box('Lime 1', background='$lime', color='black'),
                box('Indigo', name='indigo', background='$indigo', color='white'),
                box('Lime 3', background='$lime', color='black'),
                name='lime',
            ),
            col(
                box('Sky 1', background='$sky', color='black'),
                box('Sky 2', background='$sky', color='black'),
                box('Sky 3', background='$sky', color='black'),
            ),
        ),
    )

    # Insert 2 boxes before 'indigo'.
    view(
        box('Red 1', background='$lava', color='white'),
        box('Red 2', background='$lava', color='white'),
        insert=True, before='lime indigo',
    )

    # Overwrite everything after 'indigo'.
    view(
        box('Blue 1', background='$blue', color='white'),
        box('Blue 2', background='$blue', color='white'),
        after='lime indigo',
    )

    # Remove 'indigo'.
    view(remove=True, at='lime indigo')
