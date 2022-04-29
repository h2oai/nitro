# Separator



## Basic

Call `box()` with `mode='number'` to show a box with increment/decrement buttons.
(also called a *spinbox*).


```py
view(box('Donuts', mode='separator'))
```


![Screenshot](assets/screenshots/separator_basic.png)


## Set text alignment

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
