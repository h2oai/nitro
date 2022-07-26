# Layout

Compose and arrange boxes to lay out content and control flow.

## Basic

By default, items passed to `view()` are laid out one below the other.


```py
view(
    box('Top', style='border p-2'),
    box('Middle', style='border p-2'),
    box('Bottom', style='border p-2'),
)
```


![Screenshot](assets/screenshots/layout_basic.png)


## Horizontal layout

Use `row()` to lay out multiple items horizontally, left to right.


```py
view(
    row(
        box('Left', style='border p-2'),
        box('Center', style='border p-2'),
        box('Right', style='border p-2'),
    )
)
```


`row(x, y, z)` is shorthand for `box(mode='row', items=[x, y, z], style='flex flex-row gap-2')`.


```py
view(box(
    mode='row',
    items=[
        box('Left', style='border p-2'),
        box('Center', style='border p-2'),
        box('Right', style='border p-2'),
    ]
))
```


![Screenshot](assets/screenshots/layout_row.png)


## Adjust items to fit

Set the `grow` style to expand items to fit.


```py
view(
    row(
        box('Left', style='border p-2 grow'),
        box('Center', style='border p-2 grow'),
        box('Right', style='border p-2 grow'),
    )
)
```


![Screenshot](assets/screenshots/layout_grow.png)


## Adjust spacing

Set a `gap` style to change the gap between items. The default gap is `gap-2`.


```py
view(
    row(
        box('Left', style='border p-2 grow'),
        box('Center', style='border p-2 grow'),
        box('Right', style='border p-2 grow'),
        style='gap-8',
    )
)
```


![Screenshot](assets/screenshots/layout_gap.png)


## Vertical layout

Use `col()` to lay out multiple items vertically, top to bottom.

The example shows one row split into three columns containing three rows each.


```py
style = 'border p-2'
view(
    row(
        col(
            box('North-west', style=style),
            box('West', style=style),
            box('South-west', style=style),
        ),
        col(
            box('North', style=style),
            box('Center', style=style),
            box('South', style=style),
        ),
        col(
            box('North-east', style=style),
            box('East', style=style),
            box('South-east', style=style),
        ),
    ),
)
```


`col(x, y, z)` is shorthand for `box(mode='col', items=[x, y, z], style='flex flex-col gap-2')`.


```py
box(
    mode='col',
    items=[
        box(value='North'),
        box(value='Center'),
        box(value='South'),
    ]
)
```


![Screenshot](assets/screenshots/layout_col.png)


## Combine horizontal and vertical layouts

Combine `row()` and `col()` to create simple grid-like layouts

The example shows one row split into three columns containing three rows each.


```py
style = 'border p-2'
view(
    row(
        col(
            box('North-west', style=style),
            box('West', style=style),
            box('South-west', style=style),
            style='grow gap-2'
        ),
        col(
            box('North', style=style),
            box('Center', style=style),
            box('South', style=style),
            style='grow gap-2'
        ),
        col(
            box('North-east', style=style),
            box('East', style=style),
            box('South-east', style=style),
            style='grow gap-2'
        ),
        style='gap-2'
    ),
)
```


![Screenshot](assets/screenshots/layout_row_col.png)


## Tabbed layout

Set mode='tabs' on a box to lay out its items in tabs.

The `text` of each child item is used as the tab's label.


```py
view(
    box(
        mode='tabs',
        items=[
            box(
                'Profile',
                items=[
                    box('First name', value='Boaty'),
                    box('Last name', value='McBoatface'),
                    box('Age', value=42)
                ],
            ),
            box(
                'Billing Address',
                items=[
                    box('Billing address line 1', value=''),
                    box('Billing address line 2', value=''),
                    row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                ],
            ),
            box(
                'Shipping Address',
                items=[
                    box('Shipping address line 1', value=''),
                    box('Shipping address line 2', value=''),
                    row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                ],
            ),
        ]
    )
)
```


![Screenshot](assets/screenshots/layout_tabs.png)


## Accordion layout

Set `layout='col'` with `mode='tabs'` to lay out tabs one below the other, commonly known as an accordion.


```py
view(
    box(
        mode='tabs',
        layout='col',
        items=[
            box(
                'Profile',
                icon='Contact',
                items=[
                    box('First name', value='Boaty'),
                    box('Last name', value='McBoatface'),
                    box('Age', value=42)
                ],
            ),
            box(
                'Billing Address',
                icon='PaymentCard',
                items=[
                    box('Billing address line 1', value=''),
                    box('Billing address line 2', value=''),
                    row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                ],
            ),
            box(
                'Shipping Address',
                icon='DeliveryTruck',
                items=[
                    box('Shipping address line 1', value=''),
                    box('Shipping address line 2', value=''),
                    row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                ],
            ),
        ]
    )
)
```


![Screenshot](assets/screenshots/layout_tabs_vertical.png)


## Show icons on tabs

Set `icon=` on each tab to show an icon on the tab.


```py
view(
    box(
        mode='tabs',
        items=[
            box(
                'Profile',
                icon='Contact',
                items=[
                    box('First name', value='Boaty'),
                    box('Last name', value='McBoatface'),
                    box('Age', value=42)
                ],
            ),
            box(
                'Billing Address',
                icon='PaymentCard',
                items=[
                    box('Billing address line 1', value=''),
                    box('Billing address line 2', value=''),
                    row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                ],
            ),
            box(
                'Shipping Address',
                icon='DeliveryTruck',
                items=[
                    box('Shipping address line 1', value=''),
                    box('Shipping address line 2', value=''),
                    row(box('City', value=''), box('State', value=''), box('Zip', value='')),
                ],
            ),
        ]
    )
)
```


![Screenshot](assets/screenshots/layout_tabs_icons.png)


## Advanced layouts

For explicit control over layouts, use `box(items=[...])` instead of `row(...)` or `col(...)`.

The example below creates a 4-column grid layout using `style='grid'`.


```py
view(
    box(
        items=[box(f'Box {i}', style='p-2 border') for i in range(1, 13)],
        style='grid grid-cols-4 gap-2',
    )
)
```


![Screenshot](assets/screenshots/layout_grid.png)
