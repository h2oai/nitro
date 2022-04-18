# Spinbox



## Basic

Call `box()` with `mode='number'` to show a box with increment/decrement buttons.
(also called a *spinbox*).


```py
speed = view(box('Speed (km/h)', mode='number'))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/spinbox_basic.png)


## Value

Set `value=` to a numeric value to prefill the box with the value.

The mode setting `mode='number'` is implied, and can be elided.


```py
speed = view(box('Speed (km/h)', value=42))
view(f'Your speed is {speed} km/h')
```


In other words, calling `box()` with a numeric `value` has the same effect
as setting `mode='number'`, and is the preferred usage.


![Screenshot](assets/screenshots/spinbox_value.png)


## Min

Set `min=` to specify a minimum value.


```py
speed = view(box('Speed (km/h)', min=10))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/spinbox_min.png)


## Max

Set `max=` to specify a maximum value.


```py
speed = view(box('Speed (km/h)', max=100))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/spinbox_max.png)


## Step

Set `step=` to specify how much to increment or decrement by.

The default step is `1`.


```py
speed = view(box('Speed (km/h)', step=5))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/spinbox_step.png)


## Precision

Set `precision=` to specify how many decimal places the value should be rounded to.

The default is calculated based on the precision of step:

- if step = 1, precision = 0
- if step = 0.42, precision = 2
- if step = 0.0042, precision = 4


```py
speed = view(box('Speed (m/s)', value=0.6, min=-2, max=2, step=0.2, precision=2))
view(f'Your speed is {speed} m/s')
```


![Screenshot](assets/screenshots/spinbox_precision.png)


## Min, Max, Step, Precision

`min=`, `max=`, `step=` and `precision=` can be combined.


```py
speed = view(box('Speed (km/h)', min=10, max=100, step=5))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/spinbox_range.png)


## Range

Set `range=` to a `(min, max)` tuple to restrict numeric inputs between two values.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
speed = view(box('Speed (km/h)', range=(10, 100)))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/spinbox_range_alt.png)


## Range with step

Set `range=` to a `(min, max, step)` tuple to increment/decrement by steps other than `1`.

This is a shorthand notation for setting `min=`, `max=` and `step` individually.


```py
speed = view(box('Speed (km/h)', range=(10, 100, 5)))
view(f'Your speed is {speed} km/h')
```


![Screenshot](assets/screenshots/spinbox_range_alt_step.png)


## Range with precision

Setting `range=` to a `(min, max, step, precision)` tuple is a shorthand notation for setting
`min=`, `max=`, `step` and `precision` individually.


```py
speed = view(box('Speed (m/s)', value=0.6, range=(-2, 2, 0.2, 2)))
view(f'Your speed is {speed} m/s')
```


![Screenshot](assets/screenshots/spinbox_range_alt_precision.png)


## Zero-crossing range

Ranges can cross zero.


```py
speed = view(box('Speed (m/s)', value=-3, range=(-5, 5)))
view(f'Your speed is {speed} m/s')
```


![Screenshot](assets/screenshots/spinbox_negative.png)


## Fractional steps

Steps can be fractional.


```py
speed = view(box('Speed (m/s)', value=0.6, range=(-2, 2, 0.2)))
view(f'Your speed is {speed} m/s')
```


![Screenshot](assets/screenshots/spinbox_decimal_step.png)
