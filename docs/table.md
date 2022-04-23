# Table



## Basic

Call `box()` with `mode='table'` to show a table. A table can be a good substitute for a dropdown or dropdown list
when each item has several details that are better displayed in grid form.

The return value the value of selected row.


```py
x = view(box(
    mode='table',
    headers=[
        header('Flavor'),
        header('Super cheap!'),
        header('Extras'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
        option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm.']),
        option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
    ],
))
view(f'You chose {x}.')
```


![Screenshot](assets/screenshots/table_basic.png)


## Multi-select

Set `multiple=True` to allow multiple rows to be selected.

The return value is a collection of the values of the selected rows.


```py
x = view(box(
    mode='table',
    multiple=True,
    headers=[
        header('Flavor'),
        header('Super cheap!'),
        header('Extras'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
        option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm.']),
        option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
    ],
))
view(f'You chose {x}.')
```


![Screenshot](assets/screenshots/table_multiselect.png)
