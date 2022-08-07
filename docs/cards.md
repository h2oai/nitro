# Cards

Create content cards by stacking boxes together.

## Basic

```py
icon = '''
<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
</svg>
'''

def card(title, caption, score):
    return box(
        box(score,
            style='absolute top-4 right-4 rounded-full px-3 py-1.5 bg-green-100 text-green-600 font-medium text-xs'),
        col(
            box(icon, mode='svg', style='w-10 h-10'),
            box(title, style='text-xl font-bold text-gray-900'),
            box(caption, style='text-sm'),
            style='text-gray-500 pr-8',
        ),
        style='relative p-8 border shadow hover:shadow-xl rounded-xl',
    )

view(
    box(
        card(lorem(), lorem(2), '4.2'),
        card(lorem(), lorem(2), '2.6'),
        card(lorem(), lorem(2), '3.9'),
        card(lorem(), lorem(2), '5.0'),
        style='grid grid-cols-2 grid-rows-2 gap-4',
    )
)
```


![Screenshot](assets/screenshots/card_basic.png)


## With gradient border

```py
def card(title, caption):
    return box(
        box(
            box(
                box(title, style='text-xl font-bold text-gray-900'),
                box(caption, style='mt-2 text-sm text-gray-500'),
                style='mt-16 pr-8',
            ),
            style='absolute inset-1 bg-white p-8 rounded-xl'
        ),
        style='relative h-72 shadow-xl bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500 rounded-2xl',
    )

view(
    box(
        card(lorem(), lorem(2)),
        card(lorem(), lorem(2)),
        card(lorem(), lorem(2)),
        card(lorem(), lorem(2)),
        style='grid grid-cols-2 grid-rows-2 gap-4',
    )
)
```


![Screenshot](assets/screenshots/card_gradient_border.png)


## With image

```py
def card(title, caption, image):
    return box(
        box(image=image, style='object-cover w-full h-56'),
        box(
            box(title, style='text-xl font-bold'),
            box(caption, style='mt-2 text-sm text-gray-500'),
            box('Find out more →',
                style='inline-block pb-1 mt-4 font-medium text-indigo-600 border-b border-indigo-500'),
            style='p-6',
        ),
        style='overflow-hidden border border-gray-100 rounded-lg shadow-sm',
    )

view(
    box(
        card(lorem(), lorem(2), 'sample.jpg'),
        card(lorem(), lorem(2), 'sample.jpg'),
        card(lorem(), lorem(2), 'sample.jpg'),
        card(lorem(), lorem(2), 'sample.jpg'),
        style='grid grid-cols-2 grid-rows-2 gap-4',
    )
)
```


![Screenshot](assets/screenshots/card_image.png)


## Dark with image

```py
def card(category, title, caption, image):
    return box(
        box(image=image, style='object-cover w-full h-56'),
        box(
            box(category, style='text-xs text-gray-400'),
            box(title, style='text-sm text-white'),
            box(caption, style='mt-1 text-xs text-gray-300'),
            style='p-4 bg-gray-900',
        ),
        style='overflow-hidden rounded-2xl',
    )

view(
    box(
        card('Travel', lorem(), lorem(2), 'sample.jpg'),
        card('Rocketry', lorem(), lorem(2), 'sample.jpg'),
        card('Space', lorem(), lorem(2), 'sample.jpg'),
        card('Food', lorem(), lorem(2), 'sample.jpg'),
        style='grid grid-cols-2 grid-rows-2 gap-4',
    )
)
```


![Screenshot](assets/screenshots/card_dark_image.png)


## With stats

```py
view(
    box(
        row(
            box(
                box('To space and beyond', style='text-xl font-bold text-gray-900'),
                box('By Boaty McBoatface', style='mt-1 text-xs font-medium text-gray-600')
            ),
            box(
                box(image='sample.jpg', style='object-cover w-16 h-16 rounded-lg shadow-sm'),
                style='flex-shrink-0 ml-3',
            ),
            style='justify-between',
        ),
        box(lorem(7), style='mt-4 pr-12 text-sm text-gray-500'),
        row(
            box(
                box('2nd Apr 2024', style='text-xs text-gray-500'),
                box('Published', style='text-sm font-medium text-gray-600'),
            ),
            box(
                box('42 minutes', style='text-xs text-gray-500'),
                box('Reading time', style='text-sm font-medium text-gray-600'),
            ),
            style='mt-6'),
        box(style='absolute inset-x-0 bottom-0 h-2  bg-gradient-to-r from-green-300 via-blue-500 to-purple-600'),
        style='relative p-8 overflow-hidden border border-gray-100 rounded-lg',
    ),
)
```


![Screenshot](assets/screenshots/card_stats.png)
