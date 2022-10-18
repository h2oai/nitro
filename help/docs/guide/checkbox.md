---
template: overrides/main.html
---
# Checkbox

Use a checkbox to choose between two mutually exclusive options.

## Basic

Set `mode='check'` to show a checkbox.


```py
keep_signed_in = view(
    box('Keep me signed in', mode='check'),
)
view(f'Keep me signed in: {keep_signed_in}.')
```


![Screenshot](assets/screenshots/checkbox_basic.png)


## Set initial value

Set `value=True` to pre-select the checkbox.

The mode setting `mode='check'` is implied, and can be elided.


```py
keep_signed_in = view(box('Keep me signed in', value=True))
view(f'Keep me signed in: {keep_signed_in}.')
```


![Screenshot](assets/screenshots/checkbox_value.png)


## Handle changes immediately

Add `live` to `mode` to handle changes immediately.


```py
keep_signed_in = True
while True:
    keep_signed_in = view(
        box('Remember me', mode='live', value=keep_signed_in),
        "Keep me signed in." if keep_signed_in else "Don't keep me signed in.",
    )
```


![Screenshot](assets/screenshots/checkbox_live.png)


## Disable

Set `disabled=True` to disable.


```py
view(box('Keep me signed in', mode='check', disabled=True))
```


![Screenshot](assets/screenshots/checkbox_disabled.png)
