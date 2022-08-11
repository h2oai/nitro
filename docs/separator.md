# Separator

Use a separator to visually separate form inputs into sections.

## Basic

Call `box()` with `mode='separator'` to show a separator.


```py
view(box('Donuts', mode='separator'))
```


![Screenshot](assets/screenshots/separator_basic.png)


## Set text alignment

A separator's text is centered by default. Add `left`, `right`, `top`, `middle`, or `bottom` to `mode` to change the
orientation and text alignment.


```py
content = box(lorem(1), style='p-2 bg-stripes-accent')
view(
    row(
        col(
            content,
            box('Left', mode='left separator'),
            content,
        ),
        col(
            content,
            box('Center', mode='separator'),
            content,
        ),
        col(
            content,
            box('Right', mode='right separator'),
            content,
        ),
    ),
    row(
        content,
        box('Top', mode='top separator'),
        content,
        box('Middle', mode='middle separator'),
        content,
        box('Bottom', mode='bottom separator'),
        content,
    ),
)
```


![Screenshot](assets/screenshots/separator_align.png)
