# Textbox



## Basic

Call `box()` with `mode='text'` to show a textbox.

The return value is the text entered into the box.


```py
x = view(box(mode='text'))
view(f'You entered {x}.')
```


![Screenshot](assets/screenshots/textbox_basic.png)


## Value

Set `value=` to prefill the box with a value.

`mode='text'` can be elided if `value=` is set.


```py
speed = view(box(value='60 km/h'))
view(f'Your speed is {speed} km/h.')
```


![Screenshot](assets/screenshots/textbox_value.png)


## Label

Any text passed to `box()` is used as a label.


```py
speed = view(box('Speed', value='60'))
view(f'Your speed is {speed} km/h.')
```


![Screenshot](assets/screenshots/textbox_label.png)


## Placeholder

Use `placeholder=` to show placeholder text inside the box.


```py
speed = view(box('Speed', placeholder='0 km/h'))
view(f'Your speed is {speed} km/h.')
```


![Screenshot](assets/screenshots/textbox_placeholder.png)


## Required

Set `required=True` to indicate that input is required.


```py
speed = view(box('Speed (km/h)', required=True))
view(f'Your speed is {speed} km/h.')
```


![Screenshot](assets/screenshots/textbox_required.png)


## Input Mask

Set `mask=` to specify an input mask. An input mask is used to format the text field
for the expected entry.

For example, to accept a phone number, use an input mask containing three sets of digits.


```py
phone = view(box('Phone', mask='(999) 999 - 9999'))
view(f'Your phone number is {phone}.')
```


To construct the input mask:

- Use `a` to indicate a letter.
- Use `9` to indicate a number.
- Use `*` to indicate a letter or number.
- Use a backslash to escape any character.


![Screenshot](assets/screenshots/textbox_mask.png)


## Icon

Set `icon=` to show an icon at the end of the box.


```py
phrase = view(box('Filter results containing:', icon='Filter'))
view(f'You set a filter on `{phrase}`.')
```


![Screenshot](assets/screenshots/textbox_icon.png)


## Prefix

Set `prefix=` to show a prefix at the start of the box.


```py
website = view(box('Website', prefix='https://', value='example.com'))
view(f'Your website is https://{website}.')
```


![Screenshot](assets/screenshots/textbox_prefix.png)


## Suffix

Set `suffix=` to show a suffix at the end of the box.


```py
website = view(box('Website', suffix='.com', value='example'))
view(f'Your website is {website}.com.')
```


![Screenshot](assets/screenshots/textbox_suffix.png)


## Prefix and Suffix

A textbox can show both a prefix and a suffix at the same time.


```py
website = view(box('Website', prefix='https://', suffix='.com', value='example'))
view(f'Your website is https://{website}.com.')
```


![Screenshot](assets/screenshots/textbox_prefix_suffix.png)


## Error

Set `error=` to show an error message below the box.


```py
speed = view(box('Speed (km/h)', error='Invalid input'))
```


![Screenshot](assets/screenshots/textbox_error.png)


## Password

Set `password=True` when accepting passwords and other confidential inputs.


```py
password = view(box('Password field', password=True))
view(f'Your password `{password}` is not strong enough!')
```


![Screenshot](assets/screenshots/textbox_password.png)


## Multiple lines

Set `lines=` to show a multi-line text box (also called a *text area*).


```py
bio = view(box('Bio:', lines=5))
view(f'**Bio:** {bio}')
```


Note that `lines=` only controls the initial height of the textbox, and
multi-line textboxes can be resized by the user.


![Screenshot](assets/screenshots/textarea.png)
