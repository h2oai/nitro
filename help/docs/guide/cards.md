---
template: overrides/main.html
---
# Cards

Create content cards by stacking boxes together.

## Basic

```py
def card(icon, title, text, value):
    return box(
        box(value) / 'absolute top-4 right-4 rounded-full px-3 py-1.5 bg-green-100 text-green-600 font-medium text-xs',
        col(
            box(icon, mode='svg') / 'w-10 h-10',
            box(title) / 'text-xl font-bold text-gray-900',
            box(text) / 'text-sm',
        ) / 'text-gray-500 pr-8',
    ) / 'relative p-8 border shadow hover:shadow-xl rounded-xl'

icon = '''
<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
</svg>
'''
view(
    card(icon, 'To space and beyond', lorem(2), '4.2'),
    style='w-96',
)
```


![Screenshot](assets/screenshots/card_basic.png)


## With gradient border

```py
def card(title, text):
    return box(
        box(
            box(
                box(title) / 'text-xl font-bold text-gray-900',
                box(text) / 'mt-2 text-sm text-gray-500',
            ) / 'mt-16 pr-8',
        ) / 'absolute inset-1 bg-white p-8 rounded-xl',
    ) / 'relative h-72 shadow-xl bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500 rounded-2xl'

view(
    card('To space and beyond', lorem(2)),
    style='w-96',
)
```


![Screenshot](assets/screenshots/card_gradient_border.png)


## With image

```py
def card(title, text, image):
    return box(
        box(image=image) / 'object-cover w-full h-56',
        box(
            box(title) / 'text-xl font-bold',
            box(text) / 'mt-2 text-sm text-gray-500',
            box('Find out more →') / 'inline-block pb-1 mt-4 font-medium text-indigo-600 border-b border-indigo-500',
        ) / 'p-6',
    ) / 'overflow-hidden border border-gray-100 rounded-lg shadow-sm'

view(
    card('To space and beyond', lorem(2), 'sample.jpg'),
    style='w-96',
)
```


![Screenshot](assets/screenshots/card_image.png)


## Dark with image

```py
def card(tag, title, text, image):
    return box(
        box(image=image) / 'object-cover w-full h-56',
        box(
            box(tag) / 'text-xs text-gray-400',
            box(title) / 'text-sm text-white',
            box(text) / 'mt-1 text-xs text-gray-300',
        ) / 'p-4 bg-gray-900',
    ) / 'overflow-hidden rounded-2xl'

view(
    card('Rocketry', 'To space and beyond', lorem(2), 'sample.jpg'),
    style='w-96',
)
```


![Screenshot](assets/screenshots/card_dark_image.png)


## With stats

```py
def stat(label, value):
    return box(
        box(label) / 'text-xs text-gray-500',
        box(value) / 'text-sm font-medium text-gray-600',
    )

def card(title, caption, image, text, stats):
    return box(
        row(
            box(
                box(title) / 'text-xl font-bold text-gray-900',
                box(caption) / 'mt-1 text-xs font-medium text-gray-600'
            ),
            box(
                box(image=image) / 'object-cover w-16 h-16 rounded-lg shadow-sm',
            ) / 'flex-shrink-0 ml-3',
        ) / 'justify-between',
        box(text) / 'mt-4 pr-12 text-sm text-gray-500',
        row(*[stat(label, value) for label, value in stats]) / 'mt-6',
        box() / 'absolute inset-x-0 bottom-0 h-2 bg-gradient-to-r from-green-300 via-blue-500 to-purple-600',
    ) / 'relative p-8 overflow-hidden border border-gray-100 rounded-lg'

view(
    card(
        'To space and beyond',
        'By Boaty McBoatface',
        'sample.jpg',
        lorem(4),
        [
            ('Published', '2nd Apr 2024'),
            ('Reading time', '42 minutes'),
        ],
    ),
    style='w-96',
)
```


![Screenshot](assets/screenshots/card_stats.png)
