# Advanced

Learn some advanced tips and tricks to level up your Nitro skills.

## Embedding Web Pages

Set `mode='web'` to embed external web pages.


```py
view(box(mode='web', path='https://example.com'))
```


![Screenshot](assets/screenshots/embed_iframe.png)


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
