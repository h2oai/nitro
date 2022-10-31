---
template: overrides/main.html
---
# Graphics

Draw visualizations, microcharts, sparklines, and other data graphics.

## Line Y

Set `mode='g line-y'` to draw line and area charts.

For a single curve, set `data=` to a sequence of normalized y-coordinates.

For dual curves, set `data=` to a sequence of normalized `[low, high]` y-coordinates.


```py
view(row(
    # Single curve:
    col(
        # Stroke and fill:
        box(
            mode='g line-y',
            style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
            data=[0.5, 0.65, 0.5, 0.4, 0.95, 0.05, 0.5, 0.5, 0.6, 0.5, 0.5] * 6,
        ),
        # Stroke only:
        box(
            mode='g line-y',
            style='w-48 h-8 fill-none stroke-indigo-700',
            data=[0.5, 0.65, 0.5, 0.4, 0.95, 0.05, 0.5, 0.5, 0.6, 0.5, 0.5] * 6,
        ),
        # Fill only:
        box(
            mode='g line-y',
            style='w-48 h-8 fill-indigo-700 stroke-none',
            data=[0.5, 0.65, 0.5, 0.4, 0.95, 0.05, 0.5, 0.5, 0.6, 0.5, 0.5] * 6,
        ),
    ),
    # Dual curve:
    col(
        # Stroke and fill:
        box(
            mode='g line-y',
            style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
            data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
        ),

        # Stroke only:
        box(
            mode='g line-y',
            style='w-48 h-8 fill-none stroke-indigo-700',
            data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
        ),
        # Fill only:
        box(
            mode='g line-y',
            style='w-48 h-8 fill-indigo-700 stroke-none',
            data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
        ),
    ),
))
```


![Screenshot](assets/screenshots/graphics_line_y.png)


## Curve Y

Set `mode='g curve-y'` to draw line and area curves.

For a single curve, set `data=` to a sequence of normalized y-coordinates.

For dual curves, set `data=` to a sequence of normalized `[low, high]` y-coordinates.


```py
view(row(
    # Single curve:
    col(
        # Stroke and fill:
        box(
            mode='g curve-y',
            style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
            data=[0.5, 0.65, 0.5, 0.4, 0.95, 0.05, 0.5, 0.5, 0.6, 0.5, 0.5],
        ),
        # Stroke only:
        box(
            mode='g curve-y',
            style='w-48 h-8 fill-none stroke-indigo-700',
            data=[0.5, 0.65, 0.5, 0.4, 0.95, 0.05, 0.5, 0.5, 0.6, 0.5, 0.5],
        ),
        # Fill only:
        box(
            mode='g curve-y',
            style='w-48 h-8 fill-indigo-700 stroke-none',
            data=[0.5, 0.65, 0.5, 0.4, 0.95, 0.05, 0.5, 0.5, 0.6, 0.5, 0.5],
        ),
    ),
    # Dual curve:
    col(
        # Stroke and fill:
        box(
            mode='g curve-y',
            style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
            data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
        ),

        # Stroke only:
        box(
            mode='g curve-y',
            style='w-48 h-8 fill-none stroke-indigo-700',
            data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
        ),
        # Fill only:
        box(
            mode='g curve-y',
            style='w-48 h-8 fill-indigo-700 stroke-none',
            data=[[0.5, 0.8], [0.2, 0.6], [0.3, 0.9], [0.6, 0.7]] * 6,
        ),
    ),
))
```


![Screenshot](assets/screenshots/graphics_curve_y.png)


## Step Y

Set `mode='g step-y'` to draw step charts. Step charts are similar to line charts, except that adjacent points are
connected using discrete steps instead of line segments.

For a single curve, set `data=` to a sequence of normalized y-coordinates.

For dual curves, set `data=` to a sequence of normalized `[low, high]` y-coordinates.


```py
view(row(
    # Single curve:
    col(
        # Stroke and fill:
        box(
            mode='g step-y',
            style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 6,
        ),
        # Stroke only:
        box(
            mode='g step-y',
            style='w-48 h-8 fill-none stroke-indigo-700',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 6,
        ),
        # Fill only:
        box(
            mode='g step-y',
            style='w-48 h-8 fill-indigo-700 stroke-none',
            data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 6,
        ),
    ),
    # Dual curve:
    col(
        # Stroke and fill:
        box(
            mode='g step-y',
            style='w-48 h-8 fill-indigo-100 stroke-indigo-700',
            data=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]] * 6,
        ),
        # Stroke only:
        box(
            mode='g step-y',
            style='w-48 h-8 fill-none stroke-indigo-700',
            data=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]] * 6,
        ),
        # Fill only:
        box(
            mode='g step-y',
            style='w-48 h-8 fill-indigo-700 stroke-none',
            data=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]] * 6,
        ),
    ),
))
```


![Screenshot](assets/screenshots/graphics_step_y.png)


## Bar Y

Set `mode='g bar-y'` to draw bar/column charts.

For simple bars, set `data=` to a sequence of normalized y-coordinates.

For interval-valued bars, set `data=` to a sequence of normalized `[low, high]` y-coordinates.


```py
view(
    # "Column chart":
    box(
        mode='g bar-y',
        style='w-48 h-8 stroke-indigo-700',
        data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
    ),
    # Interval-valued:
    box(
        mode='g bar-y',
        style='w-48 h-8 stroke-indigo-700',
        data=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]] * 6,
    ),
)
```


![Screenshot](assets/screenshots/graphics_bar_y.png)


## Stroke Y

Set `mode='g stroke-y'` to draw a sequence of vertical strokes. The `stroke-y` mode is similar to the `bar-y`
mode, except that you can control the thickness of the strokes (bars) when using `stroke-y`.

For simple strokes, set `data=` to a sequence of normalized y-coordinates.

For interval-valued strokes, set `data=` to a sequence of normalized `[low, high]` y-coordinates.


```py
view(
    # Strokes:
    box(
        mode='g stroke-y',
        style='w-48 h-8 stroke-indigo-700',
        data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
    ),
    # Thicker strokes:
    box(
        mode='g stroke-y',
        style='w-48 h-8 stroke-indigo-700 stroke-4',
        data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
    ),
    # Interval-valued:
    box(
        mode='g stroke-y',
        style='w-48 h-8 stroke-indigo-700',
        data=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]] * 6,
    ),
)
```


![Screenshot](assets/screenshots/graphics_stroke_y.png)


## Tick Y

Set `mode='g tick-y'` to draw a sequence of horizontal ticks.

For simple ticks, set `data=` to a sequence of normalized y-coordinates.

For interval-valued ticks, set `data=` to a sequence of normalized `[low, high]` y-coordinates.


```py
view(
    # Ticks:
    box(
        mode='g tick-y',
        style='w-48 h-8 stroke-indigo-700',
        data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
    ),
    # Thicker ticks:
    box(
        mode='g tick-y',
        style='w-48 h-8 stroke-indigo-700 stroke-2',
        data=[0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 0.5] * 3,
    ),
    # Interval-valued
    box(
        mode='g tick-y',
        style='w-48 h-8 stroke-indigo-700',
        data=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]] * 6,
    ),
)
```


![Screenshot](assets/screenshots/graphics_tick_y.png)


## Guide X

Set `mode='g guide-x'` to draw a sequence of x-axis guide lines.

Set `data=` to a sequence of normalized x-coordinates.


```py
view(
    box(
        mode='g guide-x',
        style='w-48 h-8 stroke-indigo-700',
        data=[0, 0.2, 0.4, 0.6, 0.8, 0.85, 0.9, 0.95, 0.975, 1],
    ),
)
```


![Screenshot](assets/screenshots/graphics_guide_x.png)


## Guide Y

Set `mode='g guide-y'` to draw a sequence of y-axis guide lines.

Set `data=` to a sequence of normalized y-coordinates.


```py
view(
    box(
        mode='g guide-y',
        style='w-8 h-48 stroke-indigo-700',
        data=[0, 0.2, 0.4, 0.6, 0.8, 0.85, 0.9, 0.95, 0.975, 1],
    ),
)
```


![Screenshot](assets/screenshots/graphics_guide_y.png)


## Gauge X

Set `mode='g gauge-x'` to draw a horizontal gauge.

Set `data=` to normalized `[start, end, size]` values.
`size` defines the thickness of the bar relative to the rail, and defaults to 1 (bar is as thick as the rail).


```py
style = 'w-48 h-4 fill-indigo-100 stroke-indigo-700'
view(
    box(mode='g gauge-x', style=style, data=[0, 0.35]),
    box(mode='g gauge-x', style=style, data=[0.35, 1]),
    box(mode='g gauge-x', style=style, data=[0, 0.35, 0.5]),  # thinner bar
)
```


![Screenshot](assets/screenshots/graphics_gauge_x.png)


## Gauge Y

Set `mode='g gauge-y'` to draw a vertical gauge.

Set `data=` to normalized `[start, end, size]` values.
`size` defines the thickness of the bar relative to the rail, and defaults to 1 (bar is as thick as the rail).


```py
style = 'w-4 h-48 fill-indigo-100 stroke-indigo-700'
view(row(
    box(mode='g gauge-y', style=style, data=[0, 0.35]),
    box(mode='g gauge-y', style=style, data=[0.35, 1]),
    box(mode='g gauge-y', style=style, data=[0, 0.35, 0.5]),  # thinner bar
))
```


![Screenshot](assets/screenshots/graphics_gauge_y.png)


## Circular Gauge

Set `mode='g gauge-c'` to draw a circular gauge.

Set `data=` to normalized `[start-angle, end-angle, inner-radius, outer-radius, size]` values.

`inner-radius` and `outer-radius` are optional, and default to `0` and `1` respectively.

`size` defines the size of the bar relative to the rail, and defaults to 1.


```py
style = 'w-24 h-24 fill-indigo-100 stroke-indigo-700'
view(
    row(
        box(mode='g gauge-c', style=style, data=[0, 0.35]),
        box(mode='g gauge-c', style=style, data=[0, 0.35, 0.5, 1]),
        box(mode='g gauge-c', style=style, data=[0, 0.35, 0.5]),  # end-radius defaults to 1.
        box(mode='g gauge-c', style=style, data=[0, 0.35, 0.5, 1, 0.5]),  # thinner bar
        box(mode='g gauge-c', style=style, data=[0, 0.35, 0.5, 0.75]),
        box(mode='g gauge-c', style=style, data=[0.25, 0.75, 0.5, 1]),
    ),
    row(
        # With label:
        box(
            box(mode='g gauge-c', data=[0, 0.35, 0.5]) / 'absolute inset-0 fill-red-100 stroke-red-700',
            box('35%') / 'text-sm font-bold',
        ) / 'relative flex w-24 h-24 justify-center items-center',
        # Stacked:
        box(
            box(mode='g gauge-c', data=[0, 0.35, 0.5]) / 'absolute inset-0 fill-red-100 stroke-red-700',
            box(mode='g gauge-c', data=[0.35, 0.65, 0.5]) / 'absolute inset-0 fill-none stroke-red-500',
            box(mode='g gauge-c', data=[0.65, 0.8, 0.5]) / 'absolute inset-0 fill-none stroke-red-300',
        ) / 'relative w-24 h-24',
        # Concentric:
        box(
            box(mode='g gauge-c', data=[0, 0.35, 0.8, 1]) / 'absolute inset-0 fill-red-100 stroke-red-700',
            box(mode='g gauge-c', data=[0, 0.65, 0.5, 0.7]) / 'absolute inset-0 fill-blue-100 stroke-blue-700',
            box(mode='g gauge-c', data=[0, 0.85, 0.2, 0.4]) / 'absolute inset-0 fill-green-100 stroke-green-700',
        ) / 'relative w-24 h-24',
    )
)
```


![Screenshot](assets/screenshots/graphics_gauge_c.png)


## Semicircular Gauge

Set `mode='g gauge-sc'` to draw a semicircular gauge.

Set `data=` to normalized `[start-angle, end-angle, inner-radius, outer-radius, size]` values.

`inner-radius` and `outer-radius` are optional, and default to `0` and `1` respectively.

`size` defines the size of the bar relative to the rail, and defaults to 1.


```py
style = 'w-24 h-12 fill-indigo-100 stroke-indigo-700'
view(
    row(
        box(mode='g gauge-sc', style=style, data=[0, 0.35]),
        box(mode='g gauge-sc', style=style, data=[0, 0.35, 0.5, 1]),
        box(mode='g gauge-sc', style=style, data=[0, 0.35, 0.5]),  # end-radius defaults to 1.
        box(mode='g gauge-sc', style=style, data=[0, 0.35, 0.5, 1, 0.5]),  # thinner bar
        box(mode='g gauge-sc', style=style, data=[0, 0.35, 0.5, 0.75]),
        box(mode='g gauge-sc', style=style, data=[0.25, 0.75, 0.5, 1]),
    ),
    row(
        # With label:
        box(
            box(mode='g gauge-sc', data=[0, 0.35, 0.5]) / 'absolute inset-0 fill-red-100 stroke-red-700',
            box('35%') / 'text-xs font-medium',
        ) / 'relative flex w-24 h-12 justify-center items-end',
        # Stacked:
        box(
            box(mode='g gauge-sc', data=[0, 0.35, 0.5]) / 'absolute inset-0 fill-red-100 stroke-red-700',
            box(mode='g gauge-sc', data=[0.35, 0.65, 0.5]) / 'absolute inset-0 fill-none stroke-red-500',
            box(mode='g gauge-sc', data=[0.65, 0.8, 0.5]) / 'absolute inset-0 fill-none stroke-red-300',
        ) / 'relative w-24 h-12',
        # Concentric:
        box(
            box(mode='g gauge-sc', data=[0, 0.35, 0.8, 1]) / 'absolute inset-0 fill-red-100 stroke-red-700',
            box(mode='g gauge-sc', data=[0, 0.65, 0.5, 0.7]) / 'absolute inset-0 fill-blue-100 stroke-blue-700',
            box(mode='g gauge-sc', data=[0, 0.85, 0.2, 0.4]) / 'absolute inset-0 fill-green-100 stroke-green-700',
        ) / 'relative w-24 h-12',
    ),
)
```


![Screenshot](assets/screenshots/graphics_gauge_sc.png)


## Label

Set `mode='g-label'` to draw a sequence of labels.

- Set `data=` to a sequence of normalized `[x, y, text, justify, align]` values.
- Set `justify` to `0` (left), `1` (right), or omit to center (default).
- Set `align` to `0` (top), `1` (bottom), or omit to center (default).


```py
view(
    box(
        mode='g-label',
        style='w-48 h-8 text-xs bg-slate-100',
        data=[
            [0, 0.5, '0', 0],  # first label, left-justify
            [0.25, 0.5, '100'],
            [0.5, 0.5, '200'],
            [0.75, 0.5, '300'],
            [1, 0.5, '400', 1],  # last label, right-justify
        ],
    ),
    box(
        mode='g-label',
        style='w-8 h-48 text-xs bg-slate-100',
        data=[
            # All labels are right-justified
            [1, 0, '0', 1, 0],  # first label, align top
            [1, 0.25, '100', 1],
            [1, 0.5, '200', 1],
            [1, 0.75, '300', 1],
            [1, 1, '400', 1, 1],  # last label, align bottom
        ],
    ),
)
```


![Screenshot](assets/screenshots/graphics_annotation.png)


## Rectangle

Set `mode='g-rect'` to draw multiple rectangles.


```py
view(
    box(
        mode='g-rect',
        style='w-32 h-16 fill-indigo-100 stroke-indigo-700',
        data=[
            [0.1, 0.1, 0.3, 0.9],
            [0.4, 0.3, 0.6, 0.7],
            [0.7, 0.1, 0.9, 0.9, 10],
        ],
    ),
)
```


![Screenshot](assets/screenshots/graphics_rect.png)

## Win Loss

Stack two bar graphics vertically to create a win-loss graphic.


```py
wins = [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1] * 2
losses = [(x + 1) % 2 for x in wins]  # invert wins
view(
    box(
        box(mode='g bar-y', style='w-48 h-4 stroke-green-700', data=wins),
        box(mode='g bar-y', style='w-48 h-4 stroke-red-700', data=losses),
    )
)
```


![Screenshot](assets/screenshots/graphics_win_loss.png)


## Stacked bar

Overlay multiple gauges to create a stacked bar.


```py
bar = box(mode='g gauge-x') / 'absolute inset-0 fill-none'
view(
    box(
        bar(data=[0, 0.1]) / 'stroke-red-400',
        bar(data=[0.1, 0.3]) / 'stroke-orange-400',
        bar(data=[0.3, 0.7]) / 'stroke-amber-400',
        bar(data=[0.7, 0.8]) / 'stroke-lime-400',
        bar(data=[0.8, 1.0]) / 'stroke-green-400',
    ) / 'relative w-48 h-4',
)
```


![Screenshot](assets/screenshots/graphics_stacked_bar.png)


## Bullet graph

Overlay multiple gauge and guide graphics to create a bullet graph.


```py
layer = box() / 'absolute inset-0 fill-none'
bar = layer(mode='g gauge-x')
view(
    box(
        bar(data=[0, 0.6]) / 'stroke-slate-400',  # band
        bar(data=[0.6, 0.8]) / 'stroke-slate-300',  # band
        bar(data=[0.8, 1]) / 'stroke-slate-200',  # band
        bar(data=[0, 0.7, 0.25]) / 'stroke-slate-900',  # measure
        layer(mode='g guide-x', data=[0.9]) / 'stroke-red-800',  # comparative measure
    ) / 'relative w-48 h-6',
)
```


![Screenshot](assets/screenshots/graphics_bullet_graph.png)
