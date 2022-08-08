# Layout

Compose and arrange boxes to lay out content and control flow.

## Basic

By default, items passed to `view()` are laid out one below the other.


```py
style = 'p-2 rounded bg-accent-500 text-white'
view(
    box('Top', style=style),
    box('Middle', style=style),
    box('Bottom', style=style),
    style='bg-stripes-accent',
)
```


![Screenshot](assets/screenshots/layout_basic.png)


## Horizontal layout

Use `row()` to lay out multiple items horizontally, left to right.


```py
style = 'p-2 rounded bg-accent-500 text-white'
view(
    row(
        box('Left', style=style),
        box('Center', style=style),
        box('Right', style=style),
        style='bg-stripes-accent',
    )
)
```


`row(x, y, z)` is in fact shorthand for `box(x, y, z, mode='row', style='flex flex-row gap-2')`.
The following code produces the same results.


```py
style = 'p-2 rounded bg-accent-500 text-white'
view(
    box(
        box('Left', style=style),
        box('Center', style=style),
        box('Right', style=style),
        mode='row',
        style='flex flex-row gap-2 bg-stripes-accent',
    ),
)
```


![Screenshot](assets/screenshots/layout_row.png)


## Adjust items to fit

Set the `grow` style to expand items to fit.


```py
style = 'p-2 rounded bg-accent-500 text-white grow'
view(
    row(
        box('Left', style=style),
        box('Center', style=style),
        box('Right', style=style),
        style='bg-stripes-accent',
    )
)
```


![Screenshot](assets/screenshots/layout_grow.png)


## Adjust spacing

Set a `gap` style to change the gap between items. The default gap is `gap-2`.


```py
style = 'p-2 rounded bg-accent-500 text-white grow'
view(
    row(
        box('Left', style=style),
        box('Center', style=style),
        box('Right', style=style),
        style='gap-8 bg-stripes-accent',
    )
)
```


![Screenshot](assets/screenshots/layout_gap.png)


## Vertical layout

Use `col()` to lay out multiple items vertically, top to bottom.

The example shows one row split into three columns containing three rows each.


```py
style = 'p-2 rounded bg-accent-500 text-white'
view(
    col(
        box('North', style=style),
        box('Center', style=style),
        box('South', style=style),
        style='bg-stripes-accent',
    ),
)
```


`col(x, y, z)` is shorthand for `box(x, y, z, mode='col', style='flex flex-col gap-2')`.


```py
box(
    box(value='North'),
    box(value='Center'),
    box(value='South'),
    mode='col',
    style='flex flex-col gap-2',
)
```


![Screenshot](assets/screenshots/layout_col.png)


## Combine horizontal and vertical layouts

Combine `row()` and `col()` to create simple grid-like layouts

The example shows one row split into three columns containing three rows each.


```py
style = 'p-2 rounded bg-accent-500 text-white'
view(
    row(
        col(
            box('North-west', style=style),
            box('West', style=style),
            box('South-west', style=style),
            style='grow'
        ),
        col(
            box('North', style=style),
            box('Center', style=style),
            box('South', style=style),
            style='grow'
        ),
        col(
            box('North-east', style=style),
            box('East', style=style),
            box('South-east', style=style),
            style='grow'
        ),
        style='bg-stripes-accent'
    ),
)
```


![Screenshot](assets/screenshots/layout_row_col.png)


## Grid layout

A simple way to lay out items in a grid is use the `grid` style.

The example below lays out 12 boxes in a 4-column grid.


```py
style = 'p-2 rounded bg-accent-500 text-white'

# Create some boxes.
boxes = [box(f'Box {i}', style=style) for i in range(1, 13)]

# Place the boxes in a 4-column grid.
view(box(*boxes, style='grid grid-cols-4 gap-2 bg-stripes-accent'))
```


![Screenshot](assets/screenshots/layout_grid.png)


## Tabbed layout

Set `mode='tab'` on a box to lay out its items in tabs.

The `text` of each child item is used as the tab's label.


```py
view(
    box(
        box(
            box('First name', value='Boaty'),
            box('Last name', value='McBoatface'),
            box('Age', value=42),
            title='Profile',
        ),
        box(
            box('Billing address line 1', value=''),
            box('Billing address line 2', value=''),
            row(box('City', value=''), box('State', value=''), box('Zip', value='')),
            title='Billing Address',
        ),
        box(
            box('Shipping address line 1', value=''),
            box('Shipping address line 2', value=''),
            row(box('City', value=''), box('State', value=''), box('Zip', value='')),
            title='Shipping Address',
        ),
        mode='tab',
    )
)
```


![Screenshot](assets/screenshots/layout_tabs.png)


## Accordion layout

Set `mode='vertical tab'` to lay out tabs one below the other, commonly known as an accordion.


```py
view(
    box(
        box(
            box('First name', value='Boaty'),
            box('Last name', value='McBoatface'),
            box('Age', value=42),
            title='Profile',
            icon='Contact',
        ),
        box(
            box('Billing address line 1', value=''),
            box('Billing address line 2', value=''),
            row(box('City', value=''), box('State', value=''), box('Zip', value='')),
            title='Billing Address',
            icon='PaymentCard',
        ),
        box(
            box('Shipping address line 1', value=''),
            box('Shipping address line 2', value=''),
            row(box('City', value=''), box('State', value=''), box('Zip', value='')),
            title='Shipping Address',
            icon='DeliveryTruck',
        ),
        mode='vertical tab',
    )
)
```


![Screenshot](assets/screenshots/layout_tabs_vertical.png)


## Show icons on tabs

Set `icon=` on each tab to show an icon on the tab.


```py
view(
    box(
        box(
            box('First name', value='Boaty'),
            box('Last name', value='McBoatface'),
            box('Age', value=42),
            title='Profile',
            icon='Contact',
        ),
        box(
            box('Billing address line 1', value=''),
            box('Billing address line 2', value=''),
            row(box('City', value=''), box('State', value=''), box('Zip', value='')),
            title='Billing Address',
            icon='PaymentCard',
        ),
        box(
            box('Shipping address line 1', value=''),
            box('Shipping address line 2', value=''),
            row(box('City', value=''), box('State', value=''), box('Zip', value='')),
            title='Shipping Address',
            icon='DeliveryTruck',
        ),
        mode='tab',
    )
)
```


![Screenshot](assets/screenshots/layout_tabs_icons.png)
