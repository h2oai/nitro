# Help

Show context-sensitive hints and help.

## Basic

Set `help=` to associate context-sensitive help with a box.

A _hint_ (or info) icon is displayed next to the box.
Clicking on the icon displays the help content on a sidebar.


```py
choice = view(box(
    'Choose a flavor',
    mode='menu',
    options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
    help='All our flavors are 100% natural - no added sugar or colors!',
))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/help_basic.png)


## Using Markdown

`help=` supports Markdown.


```py
choice = view(box(
    'Choose a flavor',
    mode='menu',
    options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
    help='''
    ### No health risks!

    All our flavors are **100% natural** - no added sugar or colors!
    ''',
))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/help_markdown.png)


## Localization

Prefix the help with a `@` to show a locale-specific string.

For example `help='@flavor_help` shows a locale-specific string named `flavor_help`, if available.


```py
choice = view(box(
    '@flavor_caption',
    mode='menu',
    options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
    help='@flavor_help',
))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/help_localization.png)


## Hint

Set `hint=` to show an in-place pop-up hint when clicked.

Hints are a lightweight alternative to showing long-form help.
Use `hint=` instead of `help=` when you have 1-2 lines of text to display.


```py
choice = view(box(
    'Choose a flavor',
    mode='menu',
    options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
    hint='All our flavors are 100% natural - no added sugar or colors!',
))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/hint_basic.png)


## Hint with title

If the hint contains multiple lines of text, the first line is used as the title.


```py
choice = view(box(
    'Choose a flavor',
    mode='menu',
    options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
    hint='No health risks!\nAll our flavors are 100% natural - no added sugar or colors!',
))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/hint_title.png)


## Hint localization

Prefix the hint with a `@` to show a locale-specific string as the hint.

For example `hint='@flavor_hint'` shows a locale-specific string named `flavor_hint`, if available.


```py
choice = view(box(
    '@flavor_caption',
    mode='menu',
    options=['Vanilla', 'Strawberry', 'Blueberry', 'Banana'],
    hint='@flavor_hint',
))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/hint_localization.png)
