# Editing

Make changes to content already displayed on a page.

## Overview

By default, `view()` overwrites all boxes displayed by the previous `view()`.
However, you can also make `view()` selectively  append, update, insert or remove boxes.

The following example uses `insert=` or `remove=` with `before=`, `at=` or `after=`
to edit the view.


```py
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
```


![Screenshot](assets/screenshots/edit_update.png)


## Update at

Set `at=` to overwrite boxes starting at an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_update_at.png)


## Update before

Set `before=` to overwrite boxes before an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_update_before.png)


## Update after

Set `after=` to overwrite boxes after an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_update_after.png)


## Update inside

Set `inside=` to overwrite boxes inside an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_update_inside.png)


## Insert

Set `insert=True` to insert boxes into an existing view.

By default, new boxes are appended to the bottom of the view.


```py
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
```


![Screenshot](assets/screenshots/edit_insert.png)


## Insert before

Set `insert=True` with `before=` to insert boxes before an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_insert_before.png)


## Insert at

Setting `at=` has the same effect as `before=` when `Insert=True`.


```py
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
```


![Screenshot](assets/screenshots/edit_insert_at.png)


## Insert after

Set `insert=True` with `after=` to insert boxes after an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_insert_after.png)


## Insert inside

Set `insert=True` with `inside=` to insert boxes inside an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_insert_inside.png)


## Remove at

Set `remove=True` with `at=` to remove an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_remove_at.png)


## Remove before

Set `remove=True` with `before=` to remove boxes before an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_remove_before.png)


## Remove after

Set `remove=True` with `after=` to remove boxes after an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_remove_after.png)


## Remove inside

Set `remove=True` with `inside=` to remove boxes inside an existing box.


```py
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
```


![Screenshot](assets/screenshots/edit_remove_inside.png)


## Selecting nested boxes

Set `at=`, `before=`, or `after=` to space-separated names to select nested items.

- `before='foo'` means *before the box named `foo`*.
- `before='foo bar'` means *before the box named `bar` inside the box named `foo`*.
- `before='foo bar baz'` means *before the box named `baz` inside the box named `bar`, inside the box named `foo`*.
- ...and so on.


```py
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
```


![Screenshot](assets/screenshots/edit_insert_before_nested.png)
