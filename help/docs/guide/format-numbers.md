---
template: overrides/main.html
---
# Format Numbers

Language-sensitive number and currency formatting.

## Basic

Set the `num` style to format numbers.


```py
view(
    # Format using active application-wide locale.
    box('=Active: {donuts num}', data=dict(donuts=123456.789)),

    # US English
    box('=US: {donuts num}', data=dict(donuts=123456.789), locale='en-US'),

    # Germany uses comma as decimal separator and period for thousands
    box('=Germany: {donuts num}', data=dict(donuts=123456.789), locale='de-DE'),

    # Arabic in most Arabic speaking countries uses real Arabic digits
    box('=Egypt: {donuts num}', data=dict(donuts=123456.789), locale='ar-EG'),

    # India uses thousands/lakh/crore separators.
    box('=India: {donuts num}', data=dict(donuts=123456.789), locale='en-IN'),

    # Use an alternate numbering system, e.g. Chinese decimal.
    box('=China: {donuts num}', data=dict(donuts=123456.789), locale='zh-Hans-CN-u-nu-hanidec'),

    # Use Balinese if available, else fallback to Indonesian.
    box('=Indonesia: {donuts num}', data=dict(donuts=123456.789), locale=('ban', 'id')),
)
```


![Screenshot](assets/screenshots/format_number_basic.png)


## Percent

Set the `pct` style to format numbers as percentages.


```py
view(
    box('=Percent: {donuts pct}', data=dict(donuts=0.6789))
)
```


![Screenshot](assets/screenshots/format_number_percent.png)


## Scientific

Set the `sci` style to format numbers using scientific notation.


```py
view(
    box('=Donuts: {donuts sci}', data=dict(donuts=123456.789))
)
```


![Screenshot](assets/screenshots/format_number_scientific.png)


## Engineering

Set the `sci` style to format numbers using engineering notation.


```py
view(
    box('=Donuts: {donuts eng}', data=dict(donuts=123456.789))
)
```


![Screenshot](assets/screenshots/format_number_engineering.png)


## Compact

Set the `num-s` (short) or `num-xs` (extra short) style to format numbers using a compact notation.


```py
view(
    '## English',
    box('=Normal: {donuts num}', data=dict(donuts=1234567.89)),
    box('=Short: {donuts num-s}', data=dict(donuts=1234567.89)),
    box('=Extra Short: {donuts num-xs}', data=dict(donuts=1234567.89)),
    '## German',
    box('=Normal: {donuts num}', data=dict(donuts=1234567.89), locale='de'),
    box('=Short: {donuts num-s}', data=dict(donuts=1234567.89), locale='de'),
    box('=Extra Short: {donuts num-xs}', data=dict(donuts=1234567.89), locale='de'),
)
```


![Screenshot](assets/screenshots/format_number_compact.png)


## Currency

Set the `cur-*` style to format currencies.

Possible values are the ISO 4217 currency codes, such as `cur-USD` for the US dollar, `cur-EUR` for the euro,
or `cur-CNY` for the Chinese RMB
— see the [Current currency & funds code list](https://www.six-group.com/en/products-services/financial-information/data-standards.html#scrollTo=currency-codes).

Add one of `cur-l` (long), `cur-m` (medium), `cur-s` (short), `cur-xs` (extra short) styles for additional control.


```py
view(
    '## Currencies',
    box('={price cur-USD}', data=dict(price=123456.789)),
    box('={price cur-EUR}', data=dict(price=123456.789)),
    box('={price cur-RMB}', data=dict(price=123456.789)),
    '## Notation',
    box('={price cur-USD cur-l}', data=dict(price=123456.789)),
    box('={price cur-USD cur-m}', data=dict(price=123456.789)),
    box('={price cur-USD cur-s}', data=dict(price=123456.789)),
    box('={price cur-USD cur-xs}', data=dict(price=123456.789)),
)
```


![Screenshot](assets/screenshots/format_number_currency.png)


## Accounting

Set the `acc` style to wrap the number with parentheses instead of prefixing a minus sign.

Note that this feature is locale-sensitive, and might not make a difference in many locales.


```py
view(
    box('=Positive: {price cur-USD acc}', data=dict(price=123456.789)),
    box('=Negative: {price cur-USD acc}', data=dict(price=-123456.789)),

    # Makes no difference in Germany:
    box('=Negative: {price cur-EUR acc}', data=dict(price=-123456.789), locale='de'),
)
```


![Screenshot](assets/screenshots/format_number_accounting.png)


## Sign

Set a `sign-*` to control sign display.

- `sign-auto`: sign display for negative numbers only, including negative zero.
- `sign-always`: always display sign.
- `sign-except-zero`: sign display for positive and negative numbers, but not zero.
- `sign-none`: never display sign.


```py
data = [-42, '-0', 0, 42]
view(
    box('=Auto: {0 sign-auto} {1 sign-auto} {2 sign-auto} {3 sign-auto}', data=data),
    box('=Always: {0 sign-always} {1 sign-always} {2 sign-always} {3 sign-always}', data=data),
    box('=Except Zero: {0 sign-except-zero} {1 sign-except-zero} {2 sign-except-zero} {3 sign-except-zero}',
        data=data),
    box('=None: {0 sign-none} {1 sign-none} {2 sign-none} {3 sign-none}', data=data),
)
```


![Screenshot](assets/screenshots/format_number_sign.png)


## Numbering

Set a `numbering-*` style to change the numbering system.

Possible values include `arab`, `arabext`, `bali`, `beng`, `deva`, `fullwide`, `gujr`, `guru`, `hanidec`, `khmr`,
`knda`, `laoo`, `latn`, `limb`, `mlym`, `mong`, `mymr`, `orya`, `tamldec`, `telu`, `thai`, `tibt`.


```py
view(
    box('=Arabic: {donuts numbering-arab}', data=dict(donuts=123456.789)),
    box('=Devanagari: {donuts numbering-deva}', data=dict(donuts=123456.789)),
    box('=Gurumukhi: {donuts numbering-guru}', data=dict(donuts=123456.789)),
    box('=Kannada: {donuts numbering-knda}', data=dict(donuts=123456.789)),
    box('=Thai: {donuts numbering-thai}', data=dict(donuts=123456.789)),
)
```


![Screenshot](assets/screenshots/format_number_numbering.png)
