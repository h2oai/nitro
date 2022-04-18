# Dropdown List



## Basic

Set `mode='menu'` with `multiple=True` to show a dropdown menu that allows multiple options to be selected.

`mode=` can be elided when there are more than 7 options.


```py
choices = view(box(
    'Choose some colors',
    mode='menu',
    multiple=True,
    options=['green', 'yellow', 'orange', 'red']
))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/multi_dropdown_basic.png)


## Value

Set `value=` to pre-select options having those values.


```py
choices = view(box(
    'Choose some colors',
    mode='menu',
    multiple=True,
    value=['yellow', 'red'],
    options=['green', 'yellow', 'orange', 'red']
))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/multi_dropdown_value.png)


## Selected

Alternatively, set `selected=True` to pre-select one or more options.


```py
choices = view(box(
    'Choose some colors',
    mode='menu',
    multiple=True,
    options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red', selected=True),
    ]
))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/multi_dropdown_selected.png)
