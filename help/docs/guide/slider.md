---
template: overrides/main.html
---
# Slider

Use sliders to allow picking a number in a given range.

## Basic

Set `mode='range'` to show a slider.

The default range is between `0` and `10`.


```py
speed = view(box('Speed (km/h)', mode='range'))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/slider_basic.png)


## Set initial value

Set `value=` to default the slider value.


```py
speed = view(box('Speed (km/h)', mode='range', value=5))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/slider_value.png)


## Set min value

Set `min=` to specify a minimum value.


```py
speed = view(box('Speed (km/h)', mode='range', min=3))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/slider_min.png)


## Set max value

Set `max=` to specify a maximum value.


```py
speed = view(box('Speed (km/h)', mode='range', max=100))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/slider_max.png)


## Set step

Set `step=` to specify how much to increment or decrement by.

The default step is `1`.


```py
speed = view(box('Speed (km/h)', mode='range', step=2))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/slider_step.png)


## Set precision

Set `precision=` to specify how many decimal places the value should be rounded to.

The default is calculated based on the precision of step:

- if step = 1, precision = 0
- if step = 0.42, precision = 2
- if step = 0.0042, precision = 4


```py
speed = view(box('Speed (m/s)', mode='range', value=0.6, min=-2, max=2, step=0.2, precision=2))
view(f'Your speed is {speed} m/s')
```


![Screenshot](assets/screenshots/slider_precision.png)


## Combine min, max, step, precision

`min=`, `max=`, `step=` and `precision=` can be combined.


```py
speed = view(box('Speed (km/h)', mode='range', min=10, max=100, step=5))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/slider_range.png)


## Set range

Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
speed = view(box('Speed (km/h)', mode='range', range=(10, 100)))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/slider_range_alt.png)


## Set range with step

Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.

This is a shorthand notation for setting `min=`, `max=` and `step` individually.


```py
speed = view(box('Speed (km/h)', mode='range', range=(10, 100, 5)))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/slider_range_alt_step.png)


## Set range with precision

Setting `range=` to a `(min, max, step, precision)` tuple is shorthand setting
`min=`, `max=`, `step` and `precision` individually.


```py
speed = view(box('Speed (m/s)', mode='range', value=0.6, range=(-2, 2, 0.2, 2)))
view(f'Your speed is {speed} m/s')
```


![Screenshot](assets/screenshots/slider_range_alt_precision.png)


## Zero-crossing range

Ranges can cross zero.


```py
speed = view(box('Speed (m/s)', mode='range', value=-3, range=(-5, 5)))
view(f'Your speed is {speed} m/s')
```


![Screenshot](assets/screenshots/slider_negative.png)


## Set fractional steps

Steps can be fractional.


```py
speed = view(box('Speed (m/s)', mode='range', value=0.6, range=(-2, 2, 0.2)))
view(f'Your speed is {speed} m/s')
```


![Screenshot](assets/screenshots/slider_decimal_step.png)


## Handle changes immediately

Add `live` to `mode` to handle changes immediately.


```py
speed = 5  # Starting value
while True:
    speed = view(
        box('Speed (km/h)', mode='live range', value=speed),
        f'Your speed is {speed} km/h',
    )
```


![Screenshot](assets/screenshots/slider_live.png)


## Disable

Set `disabled=True` to disable.


```py
view(box('Speed (km/h)', mode='range', disabled=True))
```


![Screenshot](assets/screenshots/slider_disable.png)
