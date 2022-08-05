# Advanced

Learn some advanced tips and tricks to level up your Nitro skills.

## Embed web pages in a view

Set `mode='web'` to embed external web pages.


```py
view(box(mode='web', path='https://example.com'))
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


## An Album

A simple layout for photo galleries or portfolios.

Inspired by the [Bootstrap Album](https://getbootstrap.com/docs/4.0/examples/album/).


```py
def layout_album(view: View):  # height 11
    cards = [make_album_card(lorem(1), i) for i in range(9)]

    view(
        col(
            box(f'## {lorem()}\n\n{lorem(3)}', align='center'),
            box(dict(yes='Primary', no='Secondary'), align='center'),
            color='$background', background='$foreground',
            padding='8rem', tile='center',
        ),
        row(
            *cards,
            background='$neutral-lighter',
            wrap='between', tile='center', padding='3rem'
        ),
        gap=0,
    )


def make_album_card(text, views):
    return col(
        box(image='image.png', height=200),
        box(text, padding='0 1rem'),
        row(
            box(mode='button', options=[
                option('view', 'View', selected=False, options=[
                    option('edit', 'Edit', icon='Edit')
                ])
            ]),
            box(f'{views + 1} views', align='right', color='$neutral-secondary'),
            padding='1rem', tile='between', cross_tile='end',
        ),
        background='$background', border='$neutral-tertiary-alt',
        padding=0, width='32%',
    )
```


![Screenshot](assets/screenshots/layout_album.png)
