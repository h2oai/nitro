---
template: overrides/main.html
---
# Format

Learn the basics of formatting and templates.

## Basic

Combine _templates_ with `data=` to perform string interpolation.

A _template_ is any string that begins with a literal equals `=` symbol.

Nitro's templates are more powerful than Python's formatted string literals (f-strings) in at least two ways:

- Nitro's formatting is _locale-sensitive_. For example, if a number `123456.789` was used in a template, users in
the United States would see `123,456.789`, Germany would see `123,456.789`, and India would see `1,23,456.789`.
- You can pass _styles_ to control how each element is displayed, much like a box's visual style.
For example, the number `total` below uses the `cur-USD` currency style, which shows the number in US Dollars,
and `quota` uses the `pct` style, which shows the percentage.


```py
view(
    box(
        '=You bought {count} {product}.',
        data=dict(count=42, product='donuts'),
    ),
    box(
        '=Your total is {total cur-USD} ({quota pct} of your allowance).',
        data=dict(total=84.99, quota=0.4178978625),
    ),
)
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

    # The 'num' style is implied since 'donuts' is a number.
    box('=Default: {donuts}', data=dict(donuts=123456.789)),

    # Percent
    box('=Percent: {donuts pct}', data=dict(donuts=123456.789)),

    # Scientific notation
    box('=Scientific: {donuts sci}', data=dict(donuts=123456.789)),

    # Engineering notation
    box('=Engineering: {donuts eng}', data=dict(donuts=123456.789)),

    # Currency
    box('=Currency: {donuts cur-USD}', data=dict(donuts=123456.789)),

    # Units
    box('=Units: {donuts unit-ounce}', data=dict(donuts=123456.789)),
)
```


![Screenshot](assets/screenshots/format_number.png)


## Format date

Set the `date`, `time`, or `datetime` styles to format dates.

Advanced options are covered in a later section on date and time formatting.


```py
# Launch 100 days from now.
launch_date = (datetime.datetime.now() + datetime.timedelta(days=100)).isoformat()
view(
    box('=Launch date: {launch date}.', data=dict(launch=launch_date)),
    box('=Launch time: {launch time}.', data=dict(launch=launch_date)),
    box('=Launch date and time: {launch date time}.', data=dict(launch=launch_date)),
)
```


![Screenshot](assets/screenshots/format_date.png)


## Format lists

Set the `and`, `or`, or `list` styles to format lists.


```py
view(
    '## English',

    # Locale-sensitive list
    box('=Colors: {colors list}', data=dict(colors=['red', 'green', 'blue'])),

    # The 'list' style is implied since 'color' is a list.
    box('=Colors: {colors}', data=dict(colors=['red', 'green', 'blue'])),

    # Locale-sensitive conjunction
    box('=Colors: {colors and}', data=dict(colors=['red', 'green', 'blue'])),

    # Locale-sensitive disjunction
    box('=Colors: {colors or}', data=dict(colors=['red', 'green', 'blue'])),

    '## German',
    box('=Colors: {colors list}', data=dict(colors=['red', 'green', 'blue']), locale='de'),
    box('=Colors: {colors}', data=dict(colors=['red', 'green', 'blue']), locale='de'),
    box('=Colors: {colors and}', data=dict(colors=['red', 'green', 'blue']), locale='de'),
    box('=Colors: {colors or}', data=dict(colors=['red', 'green', 'blue']), locale='de'),

)
```


![Screenshot](assets/screenshots/format_list.png)


## Format list sizes

Suffix the `and`, `or`, or `list` styles with `-l` (long), `-s` (short), or `-xs` (extra-short)
to fine-tune formatting.


```py
view(
    '## List',
    box('=Colors: {colors list-l}', data=dict(colors=['red', 'green', 'blue'])),
    box('=Colors: {colors list-s}', data=dict(colors=['red', 'green', 'blue'])),
    box('=Colors: {colors list-xs}', data=dict(colors=['red', 'green', 'blue'])),
    '## And',
    box('=Colors: {colors and-l}', data=dict(colors=['red', 'green', 'blue'])),
    box('=Colors: {colors and-s}', data=dict(colors=['red', 'green', 'blue'])),
    box('=Colors: {colors and-xs}', data=dict(colors=['red', 'green', 'blue'])),
    '## Or',
    box('=Colors: {colors or-l}', data=dict(colors=['red', 'green', 'blue'])),
    box('=Colors: {colors or-s}', data=dict(colors=['red', 'green', 'blue'])),
    box('=Colors: {colors or-xs}', data=dict(colors=['red', 'green', 'blue'])),
)
```


![Screenshot](assets/screenshots/format_list_sizes.png)


## Format locale

Set `locale=` to change the formatting locale for a box.

Locales apply to entire blocks, i.e. any child boxes inherit the locale of the parent box, which makes it simple to
author multilingual screens using Nitro.


```py
view(
    row(
        box(
            '## English',
            box('=Normal: {donuts num}', data=dict(donuts=1234567.89)),
            box('=Short: {donuts num-s}', data=dict(donuts=1234567.89)),
            box('=Extra Short: {donuts num-xs}', data=dict(donuts=1234567.89)),
        ),
        box(
            '## German',
            box('=Normal: {donuts num}', data=dict(donuts=1234567.89)),
            box('=Short: {donuts num-s}', data=dict(donuts=1234567.89)),
            box('=Extra Short: {donuts num-xs}', data=dict(donuts=1234567.89)),
            locale='de'  # Apply locale to entire block
        ),
    ),
)
```


![Screenshot](assets/screenshots/format_locale.png)
