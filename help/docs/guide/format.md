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
    '={greeting}, {name.first} {name.last}!',
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
view(box('={0}, {1} {2}!', data=['Hello', 'Boaty', 'McBoatface']))
```


![Screenshot](assets/screenshots/format_array.png)


## Nested arrays

Combine dot-notation with 0-based integers to access nested arrays.


```py
view(box(
    '={greeting}, {name.0} {name.1}!',
    data=dict(greeting='Hello', name=['Boaty', 'McBoatface'])
))
```


![Screenshot](assets/screenshots/format_nested_array.png)


## Format number

Set the `num`, `pct`, `sci`, `eng`, `cur`, or `unit` styles to format numbers.

- `num`: decimal
- `pct`: percent
- `sci`: scientific notation
- `eng`: engineering notation
- `cur`: currency
- `unit`: units

Advanced options are covered in a later section on number formatting.


```py
view(
    # Format using active application-wide locale.
    box('=Decimal: {donuts num}', data=dict(donuts=123456.789)),
    box('=Percent: {donuts pct}', data=dict(donuts=123456.789)),
    box('=Scientific: {donuts sci}', data=dict(donuts=123456.789)),
    box('=Engineering: {donuts eng}', data=dict(donuts=123456.789)),
    box('=Currency: {donuts cur-USD}', data=dict(donuts=123456.789)),
    box('=unit: {donuts unit-ounce}', data=dict(donuts=123456.789)),
)
```


![Screenshot](assets/screenshots/format_number.png)

