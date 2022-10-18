---
template: overrides/main.html
---
# Dropdown List

Use a dropdown list to pick one or more options from a large number of options.

## Basic

Set `mode='multi menu'` to show a dropdown menu that allows multiple options to be selected.

`mode=` can be elided when there are more than 7 options.


```py
choices = view(box(
    'Choose some colors',
    mode='multi menu',
    options=['green', 'yellow', 'orange', 'red']
))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/multi_dropdown_basic.png)


## Set initial selection

Set `value=` to pre-select options having those values.


```py
choices = view(box(
    'Choose some colors',
    mode='multi menu',
    value=['yellow', 'red'],
    options=['green', 'yellow', 'orange', 'red']
))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/multi_dropdown_value.png)


## Mark options as selected

Alternatively, set `selected=True` to pre-select one or more options.


```py
choices = view(box(
    'Choose some colors',
    mode='multi menu',
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


## Handle changes immediately

Add `live` to `mode` to handle changes immediately.


```py
choices = ['green', 'yellow']
while True:
    choices = view(
        box(
            'Choose some colors',
            mode='live multi menu',
            value=choices,
            options=['green', 'yellow', 'orange', 'red'],
        ),
        f'You chose {choices}.'
    )
```


![Screenshot](assets/screenshots/multi_dropdown_live.png)


## Disable

Set `disabled=True` to disable.


```py
view(box(
    'Choose some colors',
    mode='multi menu',
    options=['green', 'yellow', 'orange', 'red'],
    disabled=True
))
```


![Screenshot](assets/screenshots/multi_dropdown_disable.png)
