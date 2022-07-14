# Context-sensitive help

Use a toggle to choose between two mutually exclusive options, with an immediate result.

## Hint

Set `hint=` to show a hint when clicked.


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


## Help

Set `help=` to show a hint when clicked.


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


## Help with Markdown

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

