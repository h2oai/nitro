# Toggle

Use a toggle to choose between two mutually exclusive options, with an immediate result.

## Basic

Set `mode='toggle'` to show a toggle.

A toggle represents a physical switch that allows someone to choose between two mutually exclusive options.
For example, “On/Off”, “Show/Hide”. Choosing an option produces an immediate result.

Note that unlike a checkbox, a toggle returns its value immediately, much like a button.
This lets you handle the changed value immediately.


```py
glazed, sprinkles, hot = True, False, False
while True:
    description = f'''
    You want your donut {"glazed" if glazed else "frosted"}, 
    {"with" if sprinkles else "without"} sprinkles, 
    and {"hot" if hot else "warm"}!
    '''
    glazed, sprinkles, hot = view(
        '### Customize my donut!',
        box('Make it glazed', mode='toggle', value=glazed),
        box('Add sprinkles', mode='toggle', value=sprinkles),
        box('Make it hot', mode='toggle', value=hot),
        description,
    )
```


![Screenshot](assets/screenshots/toggle_basic.png)
