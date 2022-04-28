# Pickers



## Basic

A *picker* is a box that allows the user to pick one or more options from several presented options, like buttons,
checklists, dropdowns, color pickers, and so on.

Set `options=` to create a picker.


```py
choice = view(box('Choose a color', options=[
    'green', 'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```


There are several ways to create options. These are explained in the next section. The simplest way is to supply a
sequence (tuple, set or list) of strings.

By default, this shows buttons for up to 3 options, radio buttons for up to 7 options,
or a dropdown menu for more than 7 options.
This behavior can be controlled using `mode=`, explained in later examples.

The example above has 4 options, hence radio buttons are shown.


![Screenshot](assets/screenshots/picker_basic.png)


## Show buttons

Buttons are shown for up to 3 options.

Set `mode='button'` to display buttons regardless of the number of options.


```py
choice = view(box('Choose a color', options=[
    'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/picker_buttons.png)


## Show radio buttons

Radio buttons is shown for 4-7 options.

Set `mode='radio'` to display radio buttons regardless of the number of options.


```py
choice = view(box('Choose a color', options=[
    'green', 'yellow', 'orange', 'red'
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/picker_radio.png)


## Show a dropdown menu

A dropdown menu is shown for more than 7 options.

Set `mode='menu'` to display a dropdown menu regardless of the number of options.


```py
choice = view(box('Choose a color', options=[
    'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/picker_dropdown.png)


## Show a dropdown list

Set `multiple=True` to allow choosing more than one option. The return value is a list of choices made.

By default, this displays checkboxes for up to 7 options, or a dropdown menu for more than 7 options.

Set `mode='menu'` to display a dropdown menu regardless of the number of options.


```py
choices = view(box('Choose some colors', multiple=True, options=[
    'violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/picker_multiple_dropdown.png)


## Show a checklist

A checklist is shown for up to 7 options when `multiple=True`.

Set `mode='check'` to display a checklist regardless of the number of options.


```py
choices = view(box('Choose some colors', mode='check', multiple=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choices}.')
```


![Screenshot](assets/screenshots/picker_checklist.png)


## Mark as required

Set `required=True` to indicate that input is required.


```py
choice = view(box('Choose a color', mode='menu', required=True, options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/picker_dropdown_required.png)


## Show an error message

Set `error=` to show an error message below the box.


```py
choice = view(box('Choose a color', mode='menu', error='Invalid input', options=[
    'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/picker_dropdown_error.png)
