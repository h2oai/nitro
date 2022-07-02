# Buttons

Use buttons to allow users to trigger actions.
They can be thought of as pickers that produce an immediate result when selected.

## Basic

Set `mode='button'` to show buttons.

`mode=` can be elided when there are 1-3 options.


```py
choice = view(box('Choose a color', mode='button', options=[
    'auto', 'yellow', 'orange', 'red',
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/buttons_basic.png)


## Shorthand notation

Most often, it doesn't make sense to show a text prompt above a set of buttons.

In such cases, `box(mode='button', options=X)` can be shortened to `box(X)`.

In other words, if the first argument to `box()` is a sequence of options, then `mode='button'` is implied.


```py
# Longer
choice = view(box(mode='button', options=['auto', 'yellow', 'orange', 'red']))

# Shorter
choice = view(box(['auto', 'yellow', 'orange', 'red']))

view(f'You chose {choice}.')
```


`options` can be a sequence of options, a sequence of tuples, or a dictionary. The following forms are equivalent:


```py
# Longer
choice = view(box([
    option('auto', 'Automatic'),
    option('yellow', 'Yellow'),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))

# Shorter
choice = view(box([
    ('auto', 'Automatic'),
    ('yellow', 'Yellow'),
    ('orange', 'Orange'),
    ('red', 'Red'),
]))

# Shortest
choice = view(box(dict(
    auto='Automatic',
    yellow='Yellow',
    orange='Orange',
    red='Red',
)))
```


![Screenshot](assets/screenshots/buttons_shorthand.png)


## Mark button as primary

By default, the first button is displayed as the primary action in the sequence.

To select a different button as primary, set `selected=True`.


```py
choice = view(
    'Updates are available!',
    box([
        option('now', 'Update now'),
        option('tomorrow', 'Remind me tomorrow', selected=True),
        option('never', 'Never update'),
    ])
)
view(f'You chose to update {choice}.')
```


![Screenshot](assets/screenshots/buttons_selected.png)


## Select primary button

Alternatively, Set `value=` to mark a button as *primary*.


```py
choice = view(
    'Updates are available!',
    box(dict(
        now='Update now',
        tomorrow='Remind me tomorrow',
        never='Never update',
    ), value='now')
)
view(f'You chose to update {choice}.')
```


![Screenshot](assets/screenshots/buttons_value.png)


## Select multiple primary buttons

If `value=` is set to a sequence, all buttons with those values are marked as *primary*.


```py
choice = view(
    'Sign me up!',
    box(dict(
        basic='Basic Plan ($9.99/month)',
        pro='Pro Plan ($14.99/month)',
        none='Not interested',
    ), value=['basic', 'pro'])
)
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/buttons_values.png)


## Add a menu

Sub-options inside options are shown as split buttons.


```py
choice = view(
    'Send fresh donuts every day?',
    box([
        option('yes', 'Yes!'),
        option('no', 'No', options=[
            option('later', 'Remind me later', icon='ChatBot'),
            option('never', "Don't ask me again", icon='MuteChat'),
        ]),
    ])
)
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/buttons_split.png)


## Add a menu to a primary button

Sub-options work for primary buttons, too.


```py
choice = view(
    'Send fresh donuts every day?',
    box([
        option('yes', 'Yes!', options=[
            option('later', 'Remind me later', icon='ChatBot'),
            option('never', "Don't ask me again", icon='MuteChat'),
        ]),
        option('no', 'No'),
    ])
)
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/buttons_selected_split.png)


## Set a caption

Set `caption=` to describe buttons.


```py
choice = view(
    'Send fresh donuts every day?',
    box([
        option('yes', 'Sign me up!', caption='Terms and conditions apply'),
        option('no', 'Not now', caption='I will decide later'),
    ])
)
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/buttons_caption.png)


## Lay out buttons vertically

By default, buttons are arranged row-wise. Set `row=False` to arrange them column-wise.


```py
choice = view(
    'Choose a color:',
    box([
        option('auto', 'Automatic'),
        option('yellow', 'Yellow'),
        option('orange', 'Orange'),
        option('red', 'Red'),
    ], row=False)
)
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/buttons_layout.png)
