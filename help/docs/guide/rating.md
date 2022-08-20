---
template: overrides/main.html
---
# Rating

Use a rating component to capture a star-rating.

## Basic

Set `mode='rating'` to accept a star-rating.

By default, five stars are displayed.


```py
stars = view(box('Rate your experience', mode='rating'))
view(f'Your rating was {stars} stars.')
```


![Screenshot](assets/screenshots/rating_basic.png)


## Set initial rating

Set `value=` to specify a default value.


```py
stars = view(box('Rate your experience', mode='rating', value=3))
view(f'Your rating was {stars} stars.')
```


![Screenshot](assets/screenshots/rating_value.png)


## Allow zero stars

Set `min=0` to allow zero stars.


```py
stars = view(box('Rate your experience', mode='rating', min=0))
view(f'Your rating was {stars} stars.')
```


![Screenshot](assets/screenshots/rating_min.png)


## Set maximum number of stars

Set `max=` to increase the number of stars displayed.


```py
stars = view(box('Rate your experience', mode='rating', value=3, max=10))
view(f'Your rating was {stars} stars.')
```


![Screenshot](assets/screenshots/rating_max.png)


## Combine min and max stars

`min=` and `max=` can be combined.


```py
stars = view(box('Rate your experience', mode='rating', value=3, min=0, max=10))
view(f'Your rating was {stars} stars.')
```


![Screenshot](assets/screenshots/rating_min_max.png)


## Set range

Set `range=` to a `(min, max)` tuple to control min/max stars.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
stars = view(box('Rate your experience', mode='rating', value=3, range=(0, 10)))
view(f'Your rating was {stars} stars.')
```


![Screenshot](assets/screenshots/rating_range.png)


## Handle changes immediately

Add `live` to `mode` to handle changes immediately.


```py
stars = 3
while True:
    stars = view(
        box('Rate your experience', mode='live rating', value=stars),
        f'Your rating was {stars} stars.'
    )
```


![Screenshot](assets/screenshots/rating_live.png)
