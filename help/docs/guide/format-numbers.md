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
