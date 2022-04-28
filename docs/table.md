# Table



## Basic

Call `box()` with `mode='table'` to show a table.


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


## Links

To make rows clickable, set `mode='link'` on a header.

If set, `view()` returns the `value` of the clicked row.


```py
choice = view(box(
    mode='table',
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


## Markdown

By default, cells are interpreted as plain text. To interpret them as markdown, set `mode='md'` on the header.


```py
choice = view(box(
    mode='table',
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


## Selectable

Set `multiple=True` to allow rows to be selected. This effectively allow a table to be used in place of a
dropdown menu, especially useful when each item has multiple attributes.

The return value is a collection of the values of the selected rows.


```py
choices = view(box(
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
    multiple=True,
))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/table_multiselect.png)


## Single-select

Set `multiple=False` to allow at most one row to be selected.

The return value is the `value` of the selected row.


```py
choice = view(box(
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
    multiple=False,
))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/table_singleselect.png)


## Value

Set `value=` to pre-select one or more rows.


```py
choices = view(box(
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
    multiple=True,
    value=['vanilla', 'blueberry'],
))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/table_value.png)


## Selected

Alternatively, set `selected=True` on a row to pre-select the row.


```py
choices = view(box(
    mode='table',
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
    multiple=True,
))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/table_selected.png)


## Grouped

To group rows, use nested options.


```py
choice = view(box(
    mode='table',
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
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/table_grouped.png)


## Multi-level Grouped

Rows can be nested at multiple levels.


```py
choice = view(box(
    mode='table',
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
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/table_multilevel.png)