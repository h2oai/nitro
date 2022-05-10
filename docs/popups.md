# Popups



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
