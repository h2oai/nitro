# Table



## Basic

Call `box()` with `mode='table'` to show a table.


```py
view(box(
    mode='table',
    headers=[
        header('Flavor'),
        header('Super cheap!'),
        header('Extras'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
        option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
        option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
    ],
))
```


![Screenshot](assets/screenshots/table_basic.png)


## Links

To make rows clickable, set `mode='link'` on a header.

If set, `view()` returns the `value` of the clicked row.


```py
choice = view(box(
    mode='table',
    headers=[
        header('Flavor', mode='link'),
        header('Super cheap!'),
        header('Extras'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', 'Sugar and spice']),
        option('sugar', options=['Powdered Sugar', '$1.99', 'Served warm']),
        option('vanilla', options=['Vanilla', '$2.99', 'With cookie crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With real blueberry']),
    ],
))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/table_clickable.png)


## Markdown

By default, cells are interpreted as plain text. To interpret them as markdown, set `mode='md'` on the header.


```py
choice = view(box(
    mode='table',
    headers=[
        header('Flavor'),
        header('Super cheap!'),
        header('Extras', mode='md'),
    ],
    options=[
        option('cinnamon', options=['Cinnamon Sugar', '$1.99', '*Sugar and spice*']),
        option('sugar', options=['Powdered Sugar', '$1.99', '**Served warm**']),
        option('vanilla',
               options=['Vanilla', '$2.99', 'With [cookie](https://en.wikipedia.org/wiki/Cookie) crumbles']),
        option('chocolate', options=['Chocolate', '$2.99', 'With sprinkles']),
        option('blueberry', options=['Blueberry', '$2.99', 'With ~real~ blueberry']),
    ],
))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/table_markdown.png)
