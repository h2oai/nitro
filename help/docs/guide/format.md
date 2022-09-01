---
template: overrides/main.html
---
# Format

Learn the basics of formatting and templates.

## Basic

Combine template strings with `data=` to perform string interpolation.

A _template string_ is any string that begins with a literal`=`.


```py
view(box('=You bought {count} {product}.', data=dict(count=42, product='donuts')))
```


![Screenshot](assets/screenshots/format_basic.png)


## Nested data

Use dot-notation to access nested data.


```py
view(box(
    '={greeting}, {name.first} {name.last}!.',
    data=dict(
        greeting='Hello',
        name=dict(
            first='Boaty',
            last='McBoatface',
        ),
    )
))
```


![Screenshot](assets/screenshots/format_nested.png)


## Arrays

Use 0-based integers to access arrays.

This notation is more compact, but less readable.


```py
view(box('={0}, {1} {2}!.', data=['Hello', 'Boaty', 'McBoatface']))
```


![Screenshot](assets/screenshots/format_array.png)


## Nested arrays

Combine dot-notation with 0-based integers to access nested arrays.


```py
view(box(
    '={greeting}, {name.0} {name.1}!.',
    data=dict(greeting='Hello', name=['Boaty', 'McBoatface'])
))
```


![Screenshot](assets/screenshots/format_nested_array.png)
