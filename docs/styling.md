# Styling

Change how boxes look: colors, borders, sizing, margins, and padding.

## Set background color

Set `background=` to apply a background color.

The text color is automatically changed to a contrasting color if not specified.
A padding is automatically applied if not specified.


```py
text = lorem(3)
view(
    box(text, background='#e63946'),
    box(text, background='#f1faee'),
    box(text, background='#a8dadc'),
    box(text, background='#457b9d'),
    box(text, background='#1d3557'),
)
```


![Screenshot](assets/screenshots/styling_background.png)
