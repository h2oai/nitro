# Week Picker



## Basic

Set `mode='week'` to show a week picker.


```py
week = view(box('Pick a week', mode='week'))
view(f'You picked {week}.')
```


![Screenshot](assets/screenshots/week_basic.png)


## Set initial week

Set `value=` to pre-select a week.

Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.


```py
week = view(box('Pick a week', mode='week', value='2021-10-10'))
view(f'You picked {week}.')
```


![Screenshot](assets/screenshots/week_value.png)


## Set min date

Set `min=` to specify a minimum date.


```py
week = view(box('Pick a week', mode='week', value='2021-10-10', min='2019-01-01'))
view(f'You picked {week}.')
```


![Screenshot](assets/screenshots/week_min.png)


## Set max date

Set `max=` to specify a maximum date.


```py
week = view(box('Pick a week', mode='week', value='2021-10-10', max='2022-12-31'))
view(f'You picked {week}.')
```


![Screenshot](assets/screenshots/week_max.png)


## Combine min and max dates

Set both `min=` and `max=` to restrict selection between two dates.


```py
week = view(box('Pick a week', mode='week', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
view(f'You picked {week}.')
```


![Screenshot](assets/screenshots/week_min_max.png)


## Set range

Set `range=` to a `(min, max)` tuple to restrict selection between two dates.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
week = view(box('Pick a week', mode='week', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
view(f'You picked {week}.')
```


![Screenshot](assets/screenshots/week_range.png)
