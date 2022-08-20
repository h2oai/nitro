---
template: overrides/main.html
---
# Calendar

Use a calendar to pick a date within a range. The calendar is an expanded form of a date picker.

## Basic

Set `mode='day'` to show a calendar.


```py
date = view(box('Pick a date', mode='day'))
view(f'You picked {date}.')
```


![Screenshot](assets/screenshots/day_basic.png)


## Set initial date

Set `value=` to pre-select a date.

Dates must be in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
Date-only strings (e.g. "1970-01-01") are treated as UTC, not local.


```py
date = view(box('Pick a date', mode='day', value='2021-10-10'))
view(f'You picked {date}.')
```


![Screenshot](assets/screenshots/day_value.png)


## Set min date

Set `min=` to specify a minimum date.


```py
date = view(box('Pick a date', mode='day', value='2021-10-10', min='2019-01-01'))
view(f'You picked {date}.')
```


![Screenshot](assets/screenshots/day_min.png)


## Set max date

Set `max=` to specify a maximum date.


```py
date = view(box('Pick a date', mode='day', value='2021-10-10', max='2022-12-31'))
view(f'You picked {date}.')
```


![Screenshot](assets/screenshots/day_max.png)


## Combine min and max dates

Set both `min=` and `max=` to restrict selection between two dates.


```py
date = view(box('Pick a date', mode='day', value='2021-10-10', min='2019-01-01', max='2022-12-31'))
view(f'You picked {date}.')
```


![Screenshot](assets/screenshots/day_min_max.png)


## Set range

Set `range=` to a `(min, max)` tuple to restrict selection between two dates.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
date = view(box('Pick a date', mode='day', value='2021-10-10', range=('2019-01-01', '2022-12-31')))
view(f'You picked {date}.')
```


![Screenshot](assets/screenshots/day_range.png)


## Handle changes immediately

Add `live` to `mode` to handle changes immediately.


```py
date = '2021-10-10'
while True:
    date = view(
        box('Pick a date', mode='live day', value=date),
        f'You picked {date} (UTC).'
    )
```


![Screenshot](assets/screenshots/day_live.png)
