# Editing



## Overview

By default, `view()` overwrites all boxes displayed by the previous `view()`,
but you can also make `view()` selectively  append, update, insert or remove boxes.

The following example uses `insert=` or `remove=` with `before=`, `at=` or `after=`
to edit the view.


```py
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
```


![Screenshot](assets/screenshots/edit_update.png)


## Update at

Set `at=` to overwrite boxes starting at an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_update_at.png)


## Update before

Set `before=` to overwrite boxes before an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_update_before.png)


## Update after

Set `after=` to overwrite boxes after an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_update_after.png)


## Insert

Set `insert=True` to insert boxes into an existing view.

By default, new boxes are appended to the bottom of the view.


```py
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
```


![Screenshot](assets/screenshots/edit_insert.png)


## Insert before

Set `insert=True` and `before=` to insert boxes before an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_insert_before.png)


## Insert at

Setting `at=` has the same effect as `before=` when `Insert=True`.


```py
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
```


![Screenshot](assets/screenshots/edit_insert_at.png)


## Insert after

Set `insert=True` and `after=` to insert boxes after an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_insert_after.png)


## Remove at

Set `remove=True` and `at=` to remove an existing box.


```py
view(
    box('Blue 1', background='$blue', color='white'),
    box('Blue 2', background='$blue', color='white'),
    box('Indigo', name='indigo', background='$indigo', color='white'),
    box('Blue 3', background='$blue', color='white'),
    box('Blue 4', background='$blue', color='white'),
)
view(remove=True, at='indigo')
```


![Screenshot](assets/screenshots/edit_remove_at.png)


## Remove before

Set `remove=True` and `before=` to remove boxes before an existing box.


```py
view(
    box('Blue 1', background='$blue', color='white'),
    box('Blue 2', background='$blue', color='white'),
    box('Indigo', name='indigo', background='$indigo', color='white'),
    box('Blue 3', background='$blue', color='white'),
    box('Blue 4', background='$blue', color='white'),
)
view(remove=True, before='indigo')
```


![Screenshot](assets/screenshots/edit_remove_before.png)


## Remove before

Set `remove=True` and `after=` to remove boxes after an existing box.


```py
view(
    box('Blue 1', background='$blue', color='white'),
    box('Blue 2', background='$blue', color='white'),
    box('Indigo', name='indigo', background='$indigo', color='white'),
    box('Blue 3', background='$blue', color='white'),
    box('Blue 4', background='$blue', color='white'),
)
view(remove=True, after='indigo')
```


![Screenshot](assets/screenshots/edit_remove_after.png)


## Selecting nested boxes

Set `at=`, `before=`, or `after=` to space-separated names to select nested items.

- `before='foo'` means *before the box named `foo`*.
- `before='foo bar'` means *before the box named `bar` inside the box named `foo`*.
- `before='foo bar baz'` means *before the box named `baz` inside the box named `bar`, inside the box named `foo`*.
- ...and so on.


```py
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
```


![Screenshot](assets/screenshots/edit_insert_before_nested.png)
