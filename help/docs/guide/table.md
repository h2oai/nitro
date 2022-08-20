---
template: overrides/main.html
---
# Table

Use tables to display detailed information in the form of a grid.
Tables can be thought of as pickers that allow one or more rows to be selected.
They are a good replacement for dropdowns and dropdown lists when each option has several displayable attributes.

## Basic

Call `box()` with `mode='table'` to show a table.

`mode` can be elided if a box has both `headers` and nested `options`.


```py
view(box(
    mode='table',
    headers=[
        header('Flavor'),
        header('Super cheap!'),
        header('Extras'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
        option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
        option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
    ],
))
```


![Screenshot](assets/screenshots/table_basic.png)


## Make rows clickable

To make rows clickable, set `mode='link'` on a header.

If set, `view()` returns the `value` of the clicked row.


```py
choice = view(box(
    headers=[
        header('Flavor', mode='link'),
        header('Super cheap!'),
        header('Extras'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
        option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
        option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
    ],
))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/table_clickable.png)


## Use markdown in cells

By default, cells are interpreted as plain text. To interpret them as markdown, set `mode='md'` on the header.


```py
choice = view(box(
    headers=[
        header('Flavor'),
        header('Super cheap!'),
        header('Extras', mode='md'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', '*Sugar and spice*']),
        option('sugar', options=['Powdered Sugar', '$1.99', '**Served warm**']),
        option('vanilla',
               options=['Vanilla', '$2.99', 'With [cookie](https://en.wikipedia.org/wiki/Cookie) crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With ~real~ blueberry']),
    ],
))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/table_markdown.png)


## Enable single select

Add `selectable` to `mode` to allow at most one row to be selected.

The `selectable table` is a good replacement for a `menu` when you need to display multiple attributes for each item.

The return value is the `value` of the selected row.


```py
choice = view(box(
    mode='selectable table',
    headers=[
        header('Flavor'),
        header('Super cheap!'),
        header('Extras'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
        option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
        option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
    ],
))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/table_singleselect.png)


## Enable multi-select

Add `multi` to `mode` to allow multiple rows to be selected.
`mode='multi table'` is shorthand for `mode='multi selectable table'`

The `multi table` is a good replacement for a `multi menu` when you need to display multiple attributes for each item.

The return value is a collection of the values of the selected rows.


```py
choices = view(box(
    mode='multi table',
    headers=[
        header('Flavor'),
        header('Super cheap!'),
        header('Extras'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
        option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
        option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
    ],
))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/table_multiselect.png)


## Set initial selection

Set `value=` to pre-select one or more rows.


```py
choices = view(box(
    mode='multi table',
    headers=[
        header('Flavor'),
        header('Super cheap!'),
        header('Extras'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
        option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
        option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
    ],
    value=['vanilla', 'blueberry'],
))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/table_value.png)


## Mark rows as selected

Alternatively, set `selected=True` on a row to pre-select the row.


```py
choices = view(box(
    mode='multi table',
    headers=[
        header('Flavor'),
        header('Super cheap!'),
        header('Extras'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
        option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
        option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles'], selected=True),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry'], selected=True),
    ],
))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/table_selected.png)


## Group rows

To group rows, use nested options.


```py
choice = view(box(
    headers=[
        header('Flavor'),
        header('Super cheap!'),
        header('Extras'),
    ],
    options=[
        option('donuts', text='Donuts', options=[
            option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
            option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
            option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
            option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
            option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
        ]),
        option('coffee', text='Coffee', options=[
            option('blonde', options=['Blonde Roast', '$1.49', 'Light and creamy']),
            option('medium', options=['Medium Roast', '$1.49', 'House favorite']),
            option('dark', options=['Dark Roast', '$1.49', 'Bold and sassy']),
        ]),
    ],
))
```


![Screenshot](assets/screenshots/table_grouped.png)


## Group rows at multiple levels

Rows can be nested at multiple levels.


```py
choice = view(box(
    headers=[
        header('Flavor'),
        header('Super cheap!'),
        header('Extras'),
    ],
    options=[
        option('donuts', text='Donuts', options=[
            option('popular', text='Popular', options=[
                option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
                option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
            ]),
            option('specialty', text='Specialty', options=[
                option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
                option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
                option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
            ]),
        ]),
        option('coffee', text='Coffee', options=[
            option('blonde', options=['Blonde Roast', '$1.49', 'Light and creamy']),
            option('medium', options=['Medium Roast', '$1.49', 'House favorite']),
            option('dark', options=['Dark Roast', '$1.49', 'Bold and sassy']),
        ]),
    ],
))
```


![Screenshot](assets/screenshots/table_multilevel.png)


## Set column width

Set `min-w-*` and `max-w-*` styles to control the minimum and maximum widths of each column.


```py
view(box(
    headers=[
        header('Flavor'),
        header('Super cheap!', style='min-w-24'),  # 96px wide
        header('Extras', style='min-w-52 max-w-72'),  # Between 208px and 288px wide
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
        option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
        option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
    ],
))
```


![Screenshot](assets/screenshots/table_column_width.png)


## Set header icon

Set `icon=` to display an icon in the header instead of text.


```py
view(box(
    headers=[
        header('Flavor'),
        header('Super cheap!', icon='Money'),
        header('Extras'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
        option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
        option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
    ],
))
```


![Screenshot](assets/screenshots/table_header_icon.png)


## Disable column resizing

Add `fixed` to `mode` to prevent a column from being resized.


```py
view(box(
    headers=[
        header('Flavor'),
        header('Super cheap!', mode='fixed'),
        header('Extras'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
        option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
        option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
    ],
))
```


![Screenshot](assets/screenshots/table_header_resizable.png)


## Enable multiline cells

Add `multiline` to `mode` to allow multiline text in a column's cells


```py
view(box(
    headers=[
        header('Flavor'),
        header('Super cheap!'),
        header('Extras', mode='multiline'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
        option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
        option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
    ],
))
```


![Screenshot](assets/screenshots/table_column_multiline.png)


## Handle changes immediately

Add `live` to `mode` to handle changes immediately.


```py
choice = 'sugar'  # Initial choice
while True:
    choice = view(
        box(
            mode='live multi table',
            value=choice,
            headers=[
                header('Flavor'),
                header('Super cheap!'),
                header('Extras'),
            ],
            options=[
                option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
                option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
                option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
                option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
                option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
            ],
        ),
        f'You chose {choice}.'
    )
```


![Screenshot](assets/screenshots/table_live.png)
