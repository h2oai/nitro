---
template: overrides/main.html
---
# Checklist

Use checkboxes to pick one or more options from a small number of options.

## Basic

Set `mode='check'` to show a checklist

`mode=` can be elided when there are 1-7 options.


```py
choices = view(box(
    'Choose some colors',
    mode='check',
    options=['green', 'yellow', 'orange', 'red']
))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/checklist_basic.png)


## Set initial selection

Set `value=` to pre-select options having those values.


```py
choices = view(box(
    'Choose some colors',
    mode='check',
    value=['yellow', 'red'],
    options=['green', 'yellow', 'orange', 'red']
))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/checklist_value.png)


## Mark options as checked

Alternatively, set `selected=True` to pre-select one or more options.


```py
choices = view(box(
    'Choose some colors',
    mode='check',
    options=[
        option('green', 'Green'),
        option('yellow', 'Yellow', selected=True),
        option('orange', 'Orange'),
        option('red', 'Red', selected=True),
    ]
))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/checklist_selected.png)


## Handle changes immediately

Add `live` to `mode` to handle changes immediately.


```py
choices = ['yellow', 'red']  # Initial selection
while True:
    choices = view(
        box(
            'Choose some colors',
            mode='live check',
            value=choices,
            options=['green', 'yellow', 'orange', 'red']
        ),
        f'You chose {choices}.'
    )
```


![Screenshot](assets/screenshots/checklist_live.png)
