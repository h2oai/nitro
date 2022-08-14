# Components

A selection of useful components that you can copy and adapt.

## Tag

Use tags to label, categorize, or organize items using keywords that describe them.


```py
def tag(label):
    return box(label) / 'border uppercase px-5 py-1.5 rounded-full text-xs tracking-wide'

def tab(color, label):
    return tag(label) / f'text-white border-{color}-500 bg-{color}-500'

def pill(color, label):
    return tag(label) / f'text-{color}-500 border-current'

def gel(color, label):
    return tag(label) / f'text-{color}-500 border-current bg-{color}-100'

view(
    row(
        tab('sky', 'Info'),
        tab('amber', 'Warning'),
        tab('green', 'Success'),
        tab('red', 'Critical'),
    ),
    row(
        pill('sky', 'Info'),
        pill('amber', 'Warning'),
        pill('green', 'Success'),
        pill('red', 'Critical'),
    ),
    row(
        gel('sky', 'Info'),
        gel('amber', 'Warning'),
        gel('green', 'Success'),
        gel('red', 'Critical'),
    ),
)
```


![Screenshot](assets/screenshots/component_tag.png)


## Badge

Alternate forms of tags, to label, categorize, or organize items.


```py
def badge(color, label, value):
    return row(
        box(f'{label}: ') / 'text-gray-700',
        box(value) / f'text-{color}-700',
    ) / 'items-center border rounded text-xs font-medium px-2.5 py-1.5'

view(
    row(
        badge('sky', 'Status', 'System available'),
        badge('amber', 'Status', 'System paused'),
        badge('green', 'Status', 'System normal'),
        badge('red', 'Status', 'System overload'),
    )
)
```


![Screenshot](assets/screenshots/component_badges.png)


## Avatar

A graphical representation of a user, team, or entity.


```py

def avatar(image, label):
    return row(
        box(image=image) / 'object-cover w-6 h-6 rounded-full',
        box(label) / 'text-xs font-medium',
    ) / 'items-center bg-gray-100 pl-2 pr-3 py-1.5 rounded-full'

view(
    row(
        avatar('sample.jpg', 'Boaty McBoatface'),
    ),
)
```


![Screenshot](assets/screenshots/component_avatar.png)


## CTA

A basic *call to action* component, typically displayed on landing pages.


```py
view(
    col(
        box('Handcrafted Espresso Drinks', mode='box'),
        box('Sipping is believing') / 'text-indigo-700',
    ) / 'text-5xl font-extrabold tracking-tight',
    box(lorem(5)) / 'mt-4',
    box(['Get Started', 'Learn More']) / 'justify-center', style='bg-gray-50 px-4 py-32 text-center',
)
```


![Screenshot](assets/screenshots/component_cta_light.png)


## Dark CTA

A basic *call to action* component for dark modes.


```py
view(
    col(
        col(
            box('Handcrafted Espresso Drinks', mode='box'),
            box('Sipping is believing', mode='box'),
        ) / 'text-5xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-green-300 via-blue-500 to-purple-600',
        box(lorem(5)) / 'mt-4',
        box(['Get Started', 'Learn More']) / 'justify-center',

    ) / 'text-white bg-gray-900 px-4 py-32 text-center',
)
```


![Screenshot](assets/screenshots/component_cta_dark.png)


## CTA with image

A basic *call to action* component with imagery.


```py
view(
    box(
        box(
            box(
                box('To space and beyond') / 'font-bold text-gray-900 text-3xl',
                box(lorem(3)) / 'text-gray-500 mt-4',
                box(box(['Get Started'])) / 'mt-8',
            ) / 'max-w-xl mx-auto',
        ) / 'px-16 py-24',
        box(image='sample.jpg') / 'object-cover w-full h-full',
    ) / 'overflow-hidden bg-gray-50 grid grid-cols-2'
)
```


![Screenshot](assets/screenshots/component_cta_image.png)


## Alert

Basic info, warning, success and failure messages.


```py
def alert(color, text):
    return box(text) / f'p-4 text-sm font-medium text-{color}-700 border-l-4 border-{color}-700 bg-{color}-50 '

view(
    alert('sky', 'Your system is up to date.'),
    alert('amber', 'A system update is available.'),
    alert('green', 'System update successful!'),
    alert('red', 'System update failed.'),
)
```


![Screenshot](assets/screenshots/component_alert_strip.png)


## Alert with description

Info, warning, success and failure messages with descriptions.


```py
def alert(color, title, text):
    return col(
        box(title) / 'text-sm font-medium',
        box(text) / 'text-xs',
    ) / f'p-4 border rounded text-{color}-700 border-{color}-200 bg-{color}-50'

view(
    alert('sky', 'Your system is up to date.', lorem(5)),
    alert('amber', 'A system update is available.', lorem(5)),
    alert('green', 'System update successful!', lorem(5)),
    alert('red', 'System update failed.', lorem(5)),
)
```


![Screenshot](assets/screenshots/component_alert.png)


## Alert with icon

Info, warning, success and failure messages with icons.


```py
def alert(color, icon, title, text):
    return row(
        box(
            box(icon, mode='svg') / 'w-5 h-5',
        ) / f'p-2 text-white bg-{color}-600 rounded-full',
        col(
            box(title) / 'text-sm font-medium',
            box(text) / 'text-xs opacity-90',
        ),
    ) / f'items-center justify-between gap-4 p-4 border rounded text-{color}-700 border-{color}-200 bg-{color}-50'

info_icon = '''
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
</svg>
'''
warning_icon = '''
 <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
 </svg>
'''
success_icon = '''
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
</svg>
'''
critical_icon = '''
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M20.618 5.984A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016zM12 9v2m0 4h.01" />
</svg>
'''

view(
    alert('sky', info_icon, 'Your system is up to date.', lorem(3)),
    alert('amber', warning_icon, 'A system update is available.', lorem(3)),
    alert('green', success_icon, 'System update successful!', lorem(3)),
    alert('red', critical_icon, 'System update failed.', lorem(3)),
)
```


![Screenshot](assets/screenshots/component_alert_icons.png)


## Pagination

Pagination is used for splitting up content or data into several pages,
with a control for navigating to the next or previous page.


```py
def link(text: str, selected: bool):
    style = 'text-white bg-indigo-600 border-indigo-600' if selected else 'border'
    return box(text, style=f'w-8 h-8 leading-8 text-center rounded {style}')

links = [link(text, text == '2') for text in ['←', '1', '2', '3', '4', '5', '→']]
view(
    row(*links) / 'justify-center gap-1 text-xs font-medium'
)
```


![Screenshot](assets/screenshots/component_pagination.png)


## Pagination with round buttons

Pagination is used for splitting up content or data into several pages,
with a control for navigating to the next or previous page.


```py
def link(text: str, selected: bool):
    style = 'text-white bg-indigo-600 border-indigo-600' if selected else 'border'
    return box(text, style=f'w-8 h-8 leading-8 text-center rounded-full {style}')

links = [link(text, text == '2') for text in ['←', '1', '2', '3', '4', '5', '→']]
view(
    row(*links) / 'justify-center gap-1 text-xs font-medium'
)
```


![Screenshot](assets/screenshots/component_pagination_round.png)


## Progress indicator

A progress indicator is a visual representation of a user’s progress through a set of steps,
guiding toward the completion of a specified process.


```py
def step(n: str, label: str, is_current: bool = False):
    color = 'text-white bg-indigo-600' if is_current else 'bg-gray-100'
    return row(
        box(n) / f'w-6 h-6 text-xs leading-6 font-bold text-center rounded-full {color}',
        box(label) / 'text-sm font-medium',
    ) / 'items-center p-2 bg-white'

view(
    box(
        box() / 'absolute bg-gray-100 top-1/2 inset-x-0 h-0.5',
        row(
            step('1', 'Cart'),
            step('2', 'Shipping', is_current=True),
            step('3', 'Payment'),
            step('4', 'Confirm'),
        ) / 'relative justify-between text-gray-500',
    ) / 'relative',
)
```


![Screenshot](assets/screenshots/component_progress_indicator.png)


## Stat

A simple stat component with a label and value.


```py
def stat(label: str, value: str):
    return col(
        box(value) / 'text-4xl font-extrabold text-indigo-600',
        box(label) / 'text-lg font-medium text-gray-500', style='gap-0 px-4 py-8 text-center border rounded-lg'
    )

view(
    box(
        stat('Donut Sales', '$4.2M'),
        stat('Flavors', '24'),
        stat('Locations', '89'),
    ) / 'grid grid-cols-3 gap-2'
)
```


![Screenshot](assets/screenshots/component_stat.png)


## Stat with icon

A stat component with an icon.


```py
icon = '''
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
</svg>
'''
view(
    box(
        row(
            box(
                box(icon, mode='svg') / 'w-8 h-8',
            ) / 'p-3 text-indigo-600 bg-indigo-100 rounded-full',
            col(
                box('$4.2M') / 'text-2xl font-medium text-gray-900',
                box('Annual Donut Sales') / 'text-sm text-gray-400',
            ) / 'gap-0',
        ) / 'items-center gap-4 p-6 bg-white border rounded-lg',
        row(
            col(
                box('$4.2M') / 'text-2xl font-medium text-gray-900',
                box('Annual Donut Sales') / 'text-sm text-gray-400',
            ) / 'gap-0',
            box(
                box(icon, mode='svg') / 'w-8 h-8',
            ) / 'p-3 text-indigo-600 bg-indigo-100 rounded-full',
        ) / 'items-center justify-between gap-4 p-6 bg-white border rounded-lg',
    ) / 'grid grid-cols-2 gap-2',
)
```


![Screenshot](assets/screenshots/component_stat_icon.png)


## Stat with change

A stat component that displays both the current value and the change in value.


```py
increase_icon = '''
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
</svg>
'''
decrease_icon = '''
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
</svg>
'''
view(
    box(
        col(
            box('Donut Sales') / 'text-sm text-gray-400',
            box('$452.2K') / 'text-2xl font-medium text-gray-900',
            row(
                box(increase_icon, mode='svg') / 'w-4 h-4 text-green-600',
                box('6.5%') / 'font-medium',
                box('Since last month') / 'text-gray-400',
            ) / 'gap-1 mt-1 text-xs',
        ) / 'gap-0 p-6 bg-white border rounded-lg',
        col(
            box('Donut Sales') / 'text-sm text-gray-400',
            box('$452.2K') / 'text-2xl font-medium text-gray-900',
            row(
                box(decrease_icon, mode='svg') / 'w-4 h-4 text-red-600',
                box('6.5%') / 'font-medium',
                box('Since last month') / 'text-gray-400',
            ) / 'gap-1 mt-1 text-xs',
        ) / 'gap-0 p-6 bg-white border rounded-lg',
    ) / 'grid grid-cols-2 gap-2',
)
```


![Screenshot](assets/screenshots/component_stat_change.png)


## Stat with floating change

A stat component that displays both the current value and the change in value.


```py
increase_icon = '''
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
</svg>
'''
decrease_icon = '''
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
</svg>
'''
view(
    box(
        row(
            box(
                box('Donut Sales') / 'text-sm text-gray-400',
                box('$452.2K') / 'text-2xl font-medium text-gray-900',
            ),
            row(
                box(increase_icon, mode='svg') / 'w-4 h-4',
                box('6.5%') / 'text-xs font-medium',
            ) / 'p-1 text-green-600 bg-green-100 rounded',
        ) / 'items-start justify-between p-6 bg-white border rounded-lg',
        row(
            box(
                box('Donut Sales') / 'text-sm text-gray-400',
                box('$452.2K') / 'text-2xl font-medium text-gray-900',
            ),
            row(
                box(decrease_icon, mode='svg') / 'w-4 h-4',
                box('6.5%') / 'text-xs font-medium',
            ) / 'p-1 text-red-600 bg-red-100 rounded',
        ) / 'items-start justify-between p-6 bg-white border rounded-lg',
    ) / 'grid grid-cols-2 gap-2',
)
```


![Screenshot](assets/screenshots/component_stat_change_floating.png)
