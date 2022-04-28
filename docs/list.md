# List



## Basic

Call `box()` with `mode='list'` to show a list. A list can be a good substitute for a dropdown menu
when each item has several details that are better displayed in tabular form.


```py
choice = view(box(
    mode='list',
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


![Screenshot](assets/screenshots/list_basic.png)


## Multi-select

Set `multiple=True` to allow multiple rows to be selected.

The return value is a collection of the values of the selected rows.


```py
choices = view(box(
    mode='list',
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


![Screenshot](assets/screenshots/list_multiselect.png)


## Value

Set `value=` to pre-select one or more rows.


```py
choices = view(box(
    mode='list',
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


![Screenshot](assets/screenshots/list_value.png)


## Selected

Alternatively, set `selected=True` on a row to pre-select the row.


```py
choices = view(box(
    mode='list',
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


![Screenshot](assets/screenshots/list_selected.png)


## Grouped

To group rows, use nested options.


```py
choice = view(box(
    mode='list',
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


![Screenshot](assets/screenshots/list_grouped.png)


## Multi-level Grouped

Rows can be nested at multiple levels.


```py
choice = view(box(
    mode='list',
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


![Screenshot](assets/screenshots/list_multilevel.png)
