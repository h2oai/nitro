---
template: overrides/main.html
---
# Color Palette

Use a color palette to pick one color from a group of colors.

## Basic

Set `options=` with `mode='color'` to show a color palette.

The option's `value` must be a valid color in one of the formats described in the previous example.

Unlike the Color Picker, the Color Palette returns the `value` of the chosen option, and not a `(r,g,b,a)` tuple.


```py
color = view(box('Choose a color', mode='color', options=[
    option('#ff0000', 'Red'),
    option('#00ff00', 'Green'),
    option('#0000ff', 'Blue'),
    option('#ffff00', 'Yellow'),
    option('#00ffff', 'Cyan'),
    option('#ff00ff', 'Magenta'),
]))
view(f'You chose {color}.')
```


![Screenshot](assets/screenshots/palette_basic.png)


## Set initial color

Set `value=` to pre-select an option having that color value.


```py
color = view(box('Choose a color', mode='color', value='#0000ff', options=[
    option('#ff0000', 'Red'),
    option('#00ff00', 'Green'),
    option('#0000ff', 'Blue'),
    option('#ffff00', 'Yellow'),
    option('#00ffff', 'Cyan'),
    option('#ff00ff', 'Magenta'),
]))
view(f'You chose {color}.')
```


![Screenshot](assets/screenshots/palette_value.png)


## Mark colors as selected

Alternatively, set `selected=True` to pre-select a color in the palette.


```py
color = view(box('Choose a color', mode='color', options=[
    option('#ff0000', 'Red'),
    option('#00ff00', 'Green'),
    option('#0000ff', 'Blue', selected=True),
    option('#ffff00', 'Yellow'),
    option('#00ffff', 'Cyan'),
    option('#ff00ff', 'Magenta'),
]))
view(f'You chose {color}.')
```


![Screenshot](assets/screenshots/palette_selected.png)


## Handle changes immediately

Add `live` to `mode` to handle changes immediately.


```py
color = '#0000ff'
while True:
    color = view(
        box(
            'Choose a color',
            mode='live color',
            value=color,
            options=[
                option('#ff0000', 'Red'),
                option('#00ff00', 'Green'),
                option('#0000ff', 'Blue'),
                option('#ffff00', 'Yellow'),
                option('#00ffff', 'Cyan'),
                option('#ff00ff', 'Magenta'),
            ],
        ),
        f'You chose {color}.'
    )
```


![Screenshot](assets/screenshots/palette_live.png)


## Disable

Set `disabled=True` to disable.


```py
view(box(
    'Choose a color',
    mode='color',
    options=[
        option('#ff0000', 'Red'),
        option('#00ff00', 'Green'),
        option('#0000ff', 'Blue'),
    ],
    disabled=True,
))
```


![Screenshot](assets/screenshots/palette_disable.png)
