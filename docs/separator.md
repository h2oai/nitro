# Separator

Use a separator to visually separate form inputs into sections.

## Basic

Call `box()` with `mode='separator'` to show a separator.


```py
view(box('Donuts', mode='separator'))
```


![Screenshot](assets/screenshots/separator_basic.png)


## Set text alignment

A separator's text is centered by default.

- Set `text-start` to show text at the start of the separator.
- Set `text-end` to show text at the end of the separator.


```py
view(
    box('Left-aligned', mode='separator text-start'),
    box(lorem(3)),
    box('Center-aligned', mode='separator'),
    box(lorem(3)),
    box('Right-aligned', mode='separator text-end'),
    box(lorem(3)),
)
```


![Screenshot](assets/screenshots/separator_align.png)


## Vertical

Set `vertical` to show a vertical separator


```py
view(
    row(
        box('Top-aligned', mode='vertical separator text-start'),
        box(lorem(3)),
        box('Center-aligned', mode='vertical separator'),
        box(lorem(3)),
        box('Bottom-aligned', mode='vertical separator text-end'),
        box(lorem(3)),
    )
)
```


![Screenshot](assets/screenshots/separator_vertical.png)
