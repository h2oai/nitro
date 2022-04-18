# Dropdown



## Basic

Set `mode='menu'` to show a dropdown menu.

`mode=` can be elided when there are more than 7 options.


```py
choice = view(box('Choose a color', mode='menu', options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/dropdown_basic.png)


## Value

Set `value=` to pre-select an option having that value.


```py
choice = view(box('Choose a color', mode='menu', value='yellow', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow'),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/dropdown_value.png)


## Selected

Set `selected=True` to pre-select an option.


```py
choice = view(box('Choose a color', mode='menu', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/dropdown_selected.png)


## Grouped

Options can have sub-options. This is useful for grouping options into categories.

`mode=menu` is implied if options are grouped.


```py
choice = view(box('Choose a color', options=[
    option('primary', 'Primary Colors', options=[
        option('red', 'Red'),
        option('blue', 'Blue'),
        option('yellow', 'Yellow'),
    ]),
    option('secondary', 'Secondary Colors', options=[
        option('violet', 'Violet'),
        option('green', 'Green'),
        option('orange', 'Orange'),
    ]),
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/dropdown_grouped.png)


## Editable

Set `editable=True` to allow arbitrary input in addition to the presented options.

`mode=menu` is implied if `editable=True`.


```py
choice = view(box('Choose a color', editable=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/dropdown_editable.png)
