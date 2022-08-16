# Layout

Compose and arrange boxes to lay out content and control flow.

## Basic

By default, items passed to `view()` are laid out one below the other.


```py
block = box() / 'p-2 rounded bg-accent-500 text-white'
view(
    block('Top'),
    block('Middle'),
    block('Bottom'),
    style='bg-stripes-accent',
)
```


![Screenshot](assets/screenshots/layout_basic.png)


## Rows

Use `row()` to lay out multiple items horizontally, left to right.


```py
block = box() / 'p-2 rounded bg-accent-500 text-white'
view(
    row(
        block('Left'),
        block('Center'),
        block('Right'),
    ) / 'bg-stripes-accent'
)
```


`row(x, y, z)` is in fact shorthand for `box(x, y, z, mode='row', style='flex flex-row gap-2')`.
The following code produces the same results.


```py
block = box() / 'p-2 rounded bg-accent-500 text-white'
view(
    box(
        block('Left'),
        block('Center'),
        block('Right'),
        mode='row',
    ) / 'flex flex-row gap-2 bg-stripes-accent',
)
```


![Screenshot](assets/screenshots/layout_row.png)


## Fit

Set the `grow` style to expand items to fit.


```py
block = box() / 'p-2 rounded bg-accent-500 text-white grow'
view(
    row(
        block('Left'),
        block('Center'),
        block('Right'),
    ) / 'bg-stripes-accent'
)
```


![Screenshot](assets/screenshots/layout_grow.png)


## Columns

Use `col()` to lay out multiple items vertically, top to bottom.

The example shows one row split into three columns containing three rows each.


```py
block = box() / 'p-2 rounded bg-accent-500 text-white'
view(
    col(
        block('North'),
        block('Center'),
        block('South'),
    ) / 'bg-stripes-accent',
)
```


`col(x, y, z)` is shorthand for `box(x, y, z, mode='col', style='flex flex-col gap-2')`.


```py
box(
    box('North'),
    box('Center'),
    box('South'),
    mode='col',
) / 'flex flex-col gap-2'
```


![Screenshot](assets/screenshots/layout_col.png)


## Combine rows and columns

Combine `row()` and `col()` to create simple grid-like layouts

The example shows one row split into three columns containing three rows each.


```py
block = box() / 'p-2 rounded bg-accent-500 text-white'
grow = col() / 'grow'  # a column stretched horizontally
view(
    row(
        grow(block('North-west'), block('West'), block('South-west')),
        grow(block('North'), block('Center'), block('South')),
        grow(block('North-east'), block('East'), block('South-east')),
    ) / 'bg-stripes-accent',
)
```


![Screenshot](assets/screenshots/layout_row_col.png)


## Grids

A simple way to lay out items in a grid is use the `grid` style.

The example below lays out 12 boxes in a 4-column grid.


```py
style = 'p-2 rounded bg-accent-500 text-white'

# Create some boxes.
boxes = [box(f'Box {i}') / style for i in range(1, 13)]

# Place the boxes in a 4-column grid.
view(box(*boxes) / 'grid grid-cols-4 gap-2 bg-stripes-accent')
```


![Screenshot](assets/screenshots/layout_grid.png)


## Groups

Add `mode='group'` or set `title=` to create a group. A group can be expanded or collapsed by the user.

A group is collapsed by default. Add `open` to `mode` to expand it.


```py
view(
    '## Menu',
    box(lorem(3), title='Donuts', mode='open'),
    box(lorem(3), title='Coffee'),
    box(lorem(3), title='Ice Cream'),
)
```


![Screenshot](assets/screenshots/layout_group.png)


## Tabs

Put groups in a row to display a tabbed layout.


```py
view(
    row(
        box(lorem(3), title='Donuts'),
        box(lorem(3), title='Coffee'),
        box(lorem(3), title='Ice Cream'),
    )
)
```


![Screenshot](assets/screenshots/layout_tabs.png)


## Vertical Tabs

Put groups in a column to display a vertical tabbed layout.


```py
view(
    col(
        box(lorem(3), title='Donuts'),
        box(lorem(3), title='Coffee'),
        box(lorem(3), title='Ice Cream'),
    )
)
```


![Screenshot](assets/screenshots/layout_tabs_vertical.png)


## Tabs with icons

Set `icon=` on each group to show an icon on its tab.


```py
view(
    row(
        box(lorem(3), title='Profile', icon='Contact'),
        box(lorem(3), title='Billing Address', icon='PaymentCard'),
        box(lorem(3), title='Shipping Address', icon='DeliveryTruck'),
    ),
)
```


![Screenshot](assets/screenshots/layout_tabs_icons.png)


## Vertical Tabs with icons

Set `icon=` on each group to show an icon on its tab.


```py
view(
    col(
        box(lorem(3), title='Profile', icon='Contact'),
        box(lorem(3), title='Billing Address', icon='PaymentCard'),
        box(lorem(3), title='Shipping Address', icon='DeliveryTruck'),
    )
)
```


![Screenshot](assets/screenshots/layout_tabs_vertical_icons.png)


## Select tab

Set a tab's `mode` to `open` to open that tab instead of the first tab in the set.


```py
view(
    row(
        box(lorem(3), title='Donuts'),
        box(lorem(3), title='Coffee', mode='open'),
        box(lorem(3), title='Ice Cream'),
    )
)
```


![Screenshot](assets/screenshots/layout_tab_select.png)


## Select vertical tab

Set a tab's `mode` to `open` to open that tab instead of the first tab in the set.


```py
view(
    col(
        box(lorem(3), title='Donuts'),
        box(lorem(3), title='Coffee', mode='open'),
        box(lorem(3), title='Ice Cream'),
    )
)
```


![Screenshot](assets/screenshots/layout_tab_vertical_select.png)
