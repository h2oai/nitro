---
template: overrides/main.html
---
# Month Picker

Use a month picker to pick a month in a given range.

## Basic

Set `mode='month'` to show a month picker.


```py
month = view(box('Pick a month', mode='month'))
view(f'You picked {month}.')
```


![Screenshot](assets/screenshots/month_basic.png)


## Set initial month

Set `value=` to pre-select a month.

Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10'))
view(f'You picked {month}.')
```


![Screenshot](assets/screenshots/month_value.png)


## Set min date

Set `min=` to specify a minimum date.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01'))
view(f'You picked {month}.')
```


![Screenshot](assets/screenshots/month_min.png)


## Set max date

Set `max=` to specify a maximum date.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10', max='2022-12-31'))
view(f'You picked {month}.')
```


![Screenshot](assets/screenshots/month_max.png)


## Combine min and max dates

Set both `min=` and `max=` to restrict selection between two dates.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
view(f'You picked {month}.')
```


![Screenshot](assets/screenshots/month_min_max.png)


## Set range

Set `range=` to a `(min, max)` tuple to restrict selection between two dates.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
month = view(box('Pick a month', mode='month', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
view(f'You picked {month}.')
```


![Screenshot](assets/screenshots/month_range.png)


## Handle changes immediately

Add `live` to `mode` to handle changes immediately.


```py
month = '2021-10-10'
while True:
    month = view(
        box('Pick a month', mode='live month', value=month),
        f'You picked {month} (UTC).'
    )
```


![Screenshot](assets/screenshots/month_live.png)
