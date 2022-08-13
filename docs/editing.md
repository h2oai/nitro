# Editing

Make changes to content already displayed on a page.

## Basics

By default, `view()` overwrites all boxes displayed by the previous `view()`.
It's also possible to selectively modify the previous view instead of overwriting it entirely.

The following example uses `view()`, `view.add()` and `view.clear()` to modify the current view.

The `at` argument indicates where to add, overwrite or clear boxes.

- `foo`: from box `foo` (or at box `foo`).
- `:foo`: before box `foo`.
- `foo:`: after box `foo`.
- `foo *`: inside box `foo`.
- `foo bar`: from box `foo`'s child box `bar` (or at box `foo`'s child box `bar`).
- `foo :bar`: before box `foo`'s child box `bar`.
- `foo bar:`: after box `foo`'s child box `bar`.
- `foo bar *`: inside box `foo`'s child box `bar`.


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
```


![Screenshot](assets/screenshots/edit_overwrite.png)


## Overwrite

Set `at='name'` to overwrite boxes starting at an existing box.


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


![Screenshot](assets/screenshots/edit_overwrite_at.png)


## Overwrite before

Set `at=':name'` to overwrite boxes before an existing box.


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
    at=':amber',
)
```


![Screenshot](assets/screenshots/edit_overwrite_before.png)


## Overwrite after

Set `at='name:'` to overwrite boxes after an existing box.


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
    at='amber:',
)
```


![Screenshot](assets/screenshots/edit_overwrite_after.png)


## Overwrite inside

Set `at='name *'` to overwrite boxes inside an existing box.


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
    at='amber *',
)
```


![Screenshot](assets/screenshots/edit_overwrite_inside.png)


## Add

Call `view.add()` to add boxes to the existing view.

By default, new boxes are appended to the bottom of the view.


```py
blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
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
```


![Screenshot](assets/screenshots/edit_add.png)


## Add before

Set `at=':name'` to add boxes before an existing box.


```py
blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
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
```


![Screenshot](assets/screenshots/edit_add_before.png)


## Add at

Setting `at='name'` has the same effect as `at=':name'` when calling `view.add()`,
i.e. "add at" is the same as "add before".


```py
blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
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
```


![Screenshot](assets/screenshots/edit_add_at.png)


## Add after

Set `at='name:'` to add boxes after an existing box.


```py
blue = part('p-2 rounded border text-sky-500 border-sky-500 bg-sky-100')
amber = part('p-2 rounded border text-amber-500 border-amber-500 bg-amber-100')
green = part('p-2 rounded border text-green-500 border-green-500 bg-green-100')
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
```


![Screenshot](assets/screenshots/edit_add_after.png)


## Add inside

Set `at='name *'` to add boxes inside an existing box.


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
view.add(
    green('Green 1'),
    green('Green 2'),
    at='amber *',
)
```


![Screenshot](assets/screenshots/edit_add_inside.png)


## Clear

Call `view.clear() to remove a box.


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
view.clear(at='red')
```


![Screenshot](assets/screenshots/edit_clear_at.png)


## Clear before

Set `at=`:name'` to clear everything before a box.


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
view.clear(at=':amber')
```


![Screenshot](assets/screenshots/edit_clear_before.png)


## Clear after

Set `at=`name:'` to clear everything after a box.


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
view.clear(at='amber:')
```


![Screenshot](assets/screenshots/edit_clear_after.png)


## Clear inside

Set `at=`name *'` to clear everything inside a box.


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
view.clear(at='amber *')
```


![Screenshot](assets/screenshots/edit_clear_inside.png)


## Selecting nested boxes

Set `at=` to space-separated names to select nested items.

- `foo` refers to the box named `foo`.
- `foo bar` refers to the box named `bar` inside the box named `foo`.
- `foo bar baz` refers to the box named `baz` inside the box named `bar` inside the box named `foo`.
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
```


![Screenshot](assets/screenshots/edit_add_before_nested.png)
