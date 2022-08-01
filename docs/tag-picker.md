# Tag Picker

Use a tag picker to pick one or more tags (short strings or labels) from a group.

## Basic

Set `mode='tag'` to display a tag picker. `multiple=True` is implied.


```py
tags = view(box(
    'Choose some tags',
    mode='tag',
    options=['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']
))
view(f'You chose {tags}.')
```


![Screenshot](assets/screenshots/tag_picker_basic.png)


## Set initial tags

Set `value=` to pre-select options having those values.


```py
tags = view(box(
    'Choose some tags',
    mode='tag',
    value=['yellow', 'red'],
    options=['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']
))
view(f'You chose {tags}.')
```


![Screenshot](assets/screenshots/tag_picker_value.png)


## Mark tags as selected

Set `selected=True` to pre-select one or more options.


```py
tags = view(box('Choose some tags', mode='tag', options=[
    option('violet', 'Violet'),
    option('indigo', 'Indigo'),
    option('blue', 'Blue'),
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red', selected=True),
]))
view(f'You chose {tags}.')
```


![Screenshot](assets/screenshots/tag_picker_selected.png)


## Handle changes immediately

Add `live` to `mode` to handle changes immediately.


```py
tags = ['yellow', 'red']
while True:
    tags = view(
        box(
            'Choose some tags',
            mode='live tag',
            value=tags,
            options=['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red'],
        ),
        f'You chose {tags}.'
    )
```


![Screenshot](assets/screenshots/tag_picker_live.png)
