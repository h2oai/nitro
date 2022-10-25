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
        style='h-8 fill-indigo-100 stroke-indigo-700',
        data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 6,
    ),
)
```


![Screenshot](assets/screenshots/graphics_line_y.png)


## Step Y

```py
view(
    box(
        mode='g step-y',
        style='h-8 fill-indigo-100 stroke-indigo-700',
        data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 6,
    ),
)
```


![Screenshot](assets/screenshots/graphics_step_y.png)


## Bar Y

```py
view(
    box(
        mode='g bar-y',
        style='h-8 fill-indigo-700',
        data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 6,
    ),
)
```


![Screenshot](assets/screenshots/graphics_bar_y.png)


## Stroke Y

```py
view(
    box(
        mode='g stroke-y',
        style='h-8 stroke-indigo-700',
        data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 12,
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
