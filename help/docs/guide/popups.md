# Popups

Display content in popup dialogs.

## Basic

Call `view()` with `popup=True` to show the view on a popup window.


```py
view(box(['Show a popup']))
view('Wait! Call us now for free donuts!', popup=True)
```


![Screenshot](assets/screenshots/popup_basic.png)


## Set popup title

Set `title=` to set a title for the popup window.


```py
view(box(['Show a popup']))
view('Call us now for free donuts!', title='Wait!', popup=True)
```


![Screenshot](assets/screenshots/popup_title.png)


## Customize buttons

If the popup's body contains a set of buttons, they're used as the popup's dismiss buttons. Common uses for such
buttons are to accept, cancel or close a popup.


```py
view(box(['Show a popup']))
response = view(
    box('Call us now for free donuts!'),
    box(options=dict(yes='Yes, now!', no='Maybe later')),
    title='Wait!', popup=True,
)
if response == 'yes':
    view('Your donuts are on the way!')
else:
    view('No donuts for you.')
```


![Screenshot](assets/screenshots/popup_buttons.png)
