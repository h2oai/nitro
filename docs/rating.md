# Rating



## Basic

Set `mode='rating'` to accept a star-rating.

By default, five stars are displayed.


```py
stars = view(box('Rate your experience', mode='rating'))
view(f'Your rating was {stars} stars.')
```


## Value

Set `value=` to specify a default value.


```py
stars = view(box('Rate your experience', mode='rating', value=3))
view(f'Your rating was {stars} stars.')
```


## Min

Set `min=0` to allow zero stars.


```py
stars = view(box('Rate your experience', mode='rating', min=0))
view(f'Your rating was {stars} stars.')
```


## Max

Set `max=` to increase the number of stars displayed.


```py
stars = view(box('Rate your experience', mode='rating', value=3, max=10))
view(f'Your rating was {stars} stars.')
```


## Min and max

`min=` and `max=` can be combined.


```py
stars = view(box('Rate your experience', mode='rating', value=3, min=0, max=10))
view(f'Your rating was {stars} stars.')
```


## Range

Set `range=` to a `(min, max)` tuple to control min/max stars.

This is a shorthand notation for setting `min=` and `max=` individually.


```py
stars = view(box('Rate your experience', mode='rating', value=3, range=(0, 10)))
view(f'Your rating was {stars} stars.')
```