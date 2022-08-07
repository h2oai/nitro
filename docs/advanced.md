# Advanced

Learn some advanced tips and tricks to level up your Nitro skills.

## Embed web pages in a view

Set `mode='web'` to embed external web pages.


```py
view(box(mode='web', path='https://example.com', style='h-96'))
```


![Screenshot](assets/screenshots/embed_iframe.png)


## Open web pages in a new view

Pass a URL to `view.jump()` with `target='_blank'` to open web pages in a new view.


```py
view('Click Continue to open https://example.com in a new view.')
view.jump('https://example.com')
```


![Screenshot](assets/screenshots/open_web_page_blank.png)


## Open web pages in a popup

URLs can be opened in popup windows by passing `popup=1`.


```py
view('Click Continue to open https://example.com in a new view.')
view.jump('https://example.com', popup=1, width=400, height=300, left=100, top=100)
```


![Screenshot](assets/screenshots/open_web_page_popup.png)


## Open web pages in the current view

Pass a URL to `view.jump()` to open web pages in the current view.


```py
view('Click Continue to open https://example.com in the current view.')
view.jump('https://example.com', target='_self')
```


![Screenshot](assets/screenshots/open_web_page.png)


## Open web pages in the top level view

Pass a URL to `view.jump()` with `target='_top'` to open web pages in the top level view.


```py
view('Click Continue to open https://example.com in the top level view.')
view.jump('https://example.com', target='_top')
```


![Screenshot](assets/screenshots/open_web_page_top.png)
