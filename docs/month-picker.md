# Month Picker



## Basic

Set `mode='month'` to show a month picker.


```py
month = view(box('Pick a month', mode='month'))
view(f'You picked {month}.')
```


![Screenshot](assets/screenshots/month_basic.png)


## Value

Set `value=` to pre-select a month.

Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10'))
view(f'You picked {month}.')
```


![Screenshot](assets/screenshots/month_value.png)


## Min

Set `min=` to specify a minimum date.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01'))
view(f'You picked {month}.')
```


![Screenshot](assets/screenshots/month_min.png)


## Max

Set `max=` to specify a maximum date.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10', max='2022-12-31'))
view(f'You picked {month}.')
```


![Screenshot](assets/screenshots/month_max.png)


## Min and Max

Set both `min=` and `max=` to restrict selection between two dates.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
view(f'You picked {month}.')
```


![Screenshot](assets/screenshots/month_min_max.png)


## Range

Set `range=` to a `(min, max)` tuple to restrict selection between two dates.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
view(f'You picked {month}.')
```


![Screenshot](assets/screenshots/month_range.png)
