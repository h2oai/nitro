# Forms

Learn the basics of collecting inputs from the user.

## Basic

To create a form, simply lay out all the inputs you need inside a view, then destructure the return value in order.


```py
username, password, action = view(
    box('Username', value='someone@company.com'),
    box('Password', value='pa55w0rd', password=True),
    box(['Login']),
)
view(f'You entered `{username}`/`{password}` and then clicked on {action}.')
```


![Screenshot](assets/screenshots/form_basic.png)


## Horizontal

Wrap items with `row()` to lay them out left to right.
There is no change to the way the return values are destructured.


```py
username, password, action = view(
    row(
        box('Username', value='someone@company.com'),
        box('Password', value='pa55w0rd', password=True),
        box(['Login']),
    )
)
view(f'You entered `{username}`/`{password}` and then clicked on {action}.')
```


![Screenshot](assets/screenshots/form_horizontal.png)


## Combined

Use `row()` and `col()` to mix and match how items are laid out. Destructure the return values in the same order.


```py
first, last, addr1, addr2, city, state, zip, action = view(
    row(box('First name', value=''), box('Last name', value='')),
    box('Address line 1', value=''),
    box('Address line 2', value=''),
    row(box('City', value=''), box('State', value=''), box('Zip', value='')),
    box([
        option('yes', 'Sign me up!'),
        option('no', 'Not now'),
    ])
)
view(f'''
You provided:

Address: {first} {last}, {addr1}, {addr2}, {city} {state} {zip}

Sign up: {action}
''')
```


![Screenshot](assets/screenshots/form_combo.png)


## Improved

Specify additional layout parameters like `width=`, `grow=`, etc. to get more control over
how items are laid out.


```py
first, middle, last, addr1, addr2, city, state, zip, action = view(
    row(box('First name', value=''), box('M.I.', value='', width='10%'), box('Last name', value='')),
    box('Address line 1', value=''),
    box('Address line 2', value=''),
    row(box('City', value='', grow=5), box('State', value='', width='20%'), box('Zip', value='', grow=1)),
    box([
        option('yes', 'Sign me up!', caption='Terms and conditions apply'),
        option('no', 'Not now', caption="I'll decide later"),
    ])
)
view(f'''
You provided:

Address: {first} {middle} {last}, {addr1}, {addr2}, {city} {state} {zip}

Sign up: {action}
''')
```


![Screenshot](assets/screenshots/form_improved.png)
