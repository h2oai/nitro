# Separator



## Basic

Call `box()` with `mode='separator'` to show a separator.


```py
view(box('Donuts', mode='separator'))
```


![Screenshot](assets/screenshots/separator_basic.png)


## Set text alignment

A separator's label is centered by default.
Set `align=` to left- or right-align the label.


```py
view(
    box('Left-aligned', mode='separator', align='left'),
    box(lorem(3)),
    box('Center-aligned', mode='separator'),
    box(lorem(3)),
    box('Right-aligned', mode='separator', align='right'),
    box(lorem(3)),
)
```


![Screenshot](assets/screenshots/separator_align.png)
