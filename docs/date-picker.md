# Date Picker



## Basic

Set `mode='date'` to show a date-picker.


```py
date = view(box('Pick a date', mode='date'))
view(f'You picked {date}.')
```


## Placeholder

Set `placeholder=` to show placeholder text.


```py
date = view(box('Deliver on', mode='date', placeholder='Delivery date'))
view(f'You picked {date}.')
```


## Required

Set `required=True` to indicate that input is required.


```py
date = view(box('Pick a date', mode='date', required=True))
view(f'You picked {date}.')
```


## Value

Set `value=` to pre-select a date.

Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.


```py
date = view(box('Pick a date', mode='date', value='2021-10-10'))
view(f'You picked {date}.')
```


## Min

Set `min=` to specify a minimum date.


```py
date = view(box('Pick a date', mode='date', value='2021-10-10', min='2019-01-01'))
view(f'You picked {date}.')
```


## Max

Set `max=` to specify a maximum date.


```py
date = view(box('Pick a date', mode='date', value='2021-10-10', max='2022-12-31'))
view(f'You picked {date}.')
```


## Min and Max

Set both `min=` and `max=` to restrict selection between two dates.


```py
date = view(box('Pick a date', mode='date', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
view(f'You picked {date}.')
```


## Range

Set `range=` to a `(min, max)` tuple to restrict selection between two dates.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
date = view(box('Pick a date', mode='date', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
view(f'You picked {date}.')
```