# Color Picker



## Basic

Set `mode='color'` to show a color picker.

The return value is a `(r, g, b, a)` tuple,
where `r`, `g`, `b` are integers between 0-255,
and `a` is an integer between 0-100%.


```py
color = view(box('Choose a color', mode='color'))
r, g, b, a = color
view(f'You chose the color `rgba({r}, {g}, {b}, {a}%)`.')
```


![Screenshot](assets/screenshots/color_basic.png)


## Value

Set `value=` to pre-select a color.

A color value can be:

- `#RRGGBB` e.g. `#ff0033`
- `#RRGGBBAA` e.g. `#ff003388`
- `#RGB` e.g. `#f03` (same as `#ff0033`)
- `#RGBA` e.g. `#f038` (same as `#ff003388`)
- `rgb(R,G,B)` e.g. `rgb(255, 0, 127)` or `rgb(100%, 0%, 50%)`
- `rgba(R,G,B,A)` e.g. `rgb(255, 0, 127, 0.5)` or `rgb(100%, 0%, 50%, 50%)`
- `hsl(H,S,L)` e.g. `hsl(348, 100%, 50%)`
- `hsl(H,S,L,A)` e.g. `hsl(348, 100%, 50%, 0.5)` or `hsl(348, 100%, 50%, 50%)`
- A [named color](https://drafts.csswg.org/css-color-3/#svg-color) e.g. `red`, `green`, `blue`, etc.
- `transparent` (same as `rgba(0,0,0,0)`)

The return value, as in the previous example, is a `(r, g, b, a)` tuple.


```py
color = view(box('Choose a color', mode='color', value='#a241e8'))
view(f'You chose {color}.')
```


![Screenshot](assets/screenshots/color_value.png)
