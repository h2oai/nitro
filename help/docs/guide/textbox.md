---
template: overrides/main.html
---
# Textbox

Use textboxes to capture text inputs and passwords.

## Basic

Call `box()` with `mode='text'` to show a textbox.

The return value is the text entered into the box.


```py
x = view(box(mode='text'))
view(f'You entered {x}.')
```


![Screenshot](assets/screenshots/textbox_basic.png)


## Set initial value

Set `value=` to prefill the box with a value.

`mode='text'` can be elided if `value=` is set.


```py
speed = view(box(value='60 km/h'))
view(f'Your speed is {speed}.')
```


![Screenshot](assets/screenshots/textbox_value.png)


## Set a label

Any text passed to `box()` is used as a label.


```py
speed = view(box('Speed', value='60'))
view(f'Your speed is {speed} km/h.')
```


![Screenshot](assets/screenshots/textbox_label.png)


## Show placeholder text

Use `placeholder=` to show placeholder text inside the box.


```py
speed = view(box('Speed', placeholder='0 km/h'))
view(f'Your speed is {speed} km/h.')
```


![Screenshot](assets/screenshots/textbox_placeholder.png)


## Mark as required

Add `required` to `mode` to indicate that input is required.


```py
speed = view(box('Speed (km/h)', mode='required'))
view(f'Your speed is {speed} km/h.')
```


![Screenshot](assets/screenshots/textbox_required.png)


## Control input format

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


## Show an icon

Set `icon=` to show an icon at the end of the box.


```py
phrase = view(box('Filter results containing:', icon='Filter'))
view(f'You set a filter on `{phrase}`.')
```


![Screenshot](assets/screenshots/textbox_icon.png)


## Set prefix text

Set `prefix=` to show a prefix at the start of the box.


```py
website = view(box('Website', prefix='https://', value='example.com'))
view(f'Your website is https://{website}.')
```


![Screenshot](assets/screenshots/textbox_prefix.png)


## Set suffix text

Set `suffix=` to show a suffix at the end of the box.


```py
website = view(box('Website', suffix='.com', value='example'))
view(f'Your website is {website}.com.')
```


![Screenshot](assets/screenshots/textbox_suffix.png)


## Set both prefix and suffix texts

A textbox can show both a prefix and a suffix at the same time.


```py
website = view(box('Website', prefix='https://', suffix='.com', value='example'))
view(f'Your website is https://{website}.com.')
```


![Screenshot](assets/screenshots/textbox_prefix_suffix.png)


## Show an error message

Set `error=` to show an error message below the box.


```py
speed = view(box('Speed (km/h)', error='Invalid input'))
```


![Screenshot](assets/screenshots/textbox_error.png)


## Accept a password

Add `password` to `mode` when accepting passwords and other confidential inputs.


```py
password = view(box('Password field', mode='password'))
view(f'Your password `{password}` is not strong enough!')
```


![Screenshot](assets/screenshots/textbox_password.png)


## Enable multiple lines

Set `lines=` to show a multi-line text box (also called a *text area*).


```py
bio = view(box('Bio:', lines=5))
view(f'**Bio:** {bio}')
```


Note that multi-line textboxes can be resized by the user,
and `lines=` only sets the initial height of the textbox.


![Screenshot](assets/screenshots/textarea.png)
