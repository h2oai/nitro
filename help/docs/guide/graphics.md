---
template: overrides/main.html
---
# Graphics

Draw microcharts, sparklines, and other data graphics.

## Line Y

```py
view(
    box(
        mode='g line-y',
        style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
        data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 6,
    ),
    box(
        mode='g line-y',
        style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
        data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
    ),
)
```


![Screenshot](assets/screenshots/graphics_line_y.png)


## Step Y

```py
view(
    box(
        mode='g step-y',
        style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
        data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 6,
    ),
    box(
        mode='g step-y',
        style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
        data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
    ),
)
```


![Screenshot](assets/screenshots/graphics_step_y.png)


## Interval Y

```py
view(
    box(
        mode='g interval-y',
        style='w-48 h-8 stroke-indigo-700',
        data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
    ),
    box(
        mode='g interval-y',
        style='w-48 h-8 stroke-indigo-700',
        data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
    ),
)
```


![Screenshot](assets/screenshots/graphics_interval_y.png)


## Stroke Y

```py
view(
    box(
        mode='g stroke-y',
        style='w-48 h-8 stroke-indigo-700',
        data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
    ),
    box(
        mode='g stroke-y',
        style='w-48 h-8 stroke-indigo-700',
        data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
    ),
)
```


![Screenshot](assets/screenshots/graphics_stroke_y.png)


## Tick Y

```py
view(
    box(
        mode='g tick-y',
        style='h-8 stroke-indigo-700',
        data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 12,
    ),
)
```


![Screenshot](assets/screenshots/graphics_tick_y.png)


## Guide X

```py
view(
    box(
        mode='g guide-x',
        style='h-8 stroke-indigo-700',
        data=[0, 0.2, 0.4, 0.6, 0.8, 0.85, 0.9, 0.95, 0.975, 1],
    ),
)
```


![Screenshot](assets/screenshots/graphics_guide_x.png)


## Guide Y

```py
view(
    box(
        mode='g guide-y',
        style='h-48 w-8 stroke-indigo-700',
        data=[0, 0.2, 0.4, 0.6, 0.8, 0.85, 0.9, 0.95, 0.975, 1],
    ),
)
```


![Screenshot](assets/screenshots/graphics_guide_y.png)


## Bar X

```py
style = 'w-48 h-2 fill-indigo-100 stroke-indigo-700'
view(
    box(mode='g bar-x', style=style, data=[0, 0.35]),
    box(mode='g bar-x', style=style, data=[0.35, 1]),
)
```


![Screenshot](assets/screenshots/graphics_bar_x.png)


## Bar Y

```py
style = 'w-2 h-48 fill-indigo-100 stroke-indigo-700'
view(row(
    box(mode='g bar-y', style=style, data=[0, 0.35]),
    box(mode='g bar-y', style=style, data=[0.35, 1]),
))
```


![Screenshot](assets/screenshots/graphics_bar_y.png)


## Circle

```py
style = 'w-24 h-24 fill-indigo-100 stroke-indigo-700'
view(row(
    box(mode='g circle', style=style, data=[0, 0.35]),
    box(mode='g circle', style=style, data=[0, 0.35, 0.5, 1]),
    box(mode='g circle', style=style, data=[0, 0.35, 0.5]),
    box(mode='g circle', style=style, data=[0, 0.35, 0.5, 0.75]),
    box(mode='g circle', style=style, data=[1, 0.35, 0.5, 1]),
))
```


![Screenshot](assets/screenshots/graphics_circle.png)


## Arc

```py
style = 'w-24 h-12 fill-indigo-100 stroke-indigo-700'
view(row(
    box(mode='g arc', style=style, data=[0, 0.35]),
    box(mode='g arc', style=style, data=[0, 0.35, 0.5, 1]),
    box(mode='g arc', style=style, data=[0, 0.35, 0.5]),
    box(mode='g arc', style=style, data=[0, 0.35, 0.5, 0.75]),
    box(mode='g arc', style=style, data=[1, 0.35, 0.5, 1]),
))
```


![Screenshot](assets/screenshots/graphics_arc.png)
