# Radio Buttons

Use radio buttons to pick one option from a small number of options.

## Basic

Set `mode='radio'` to show radio buttons.

`mode=` can be elided when there are 4-7 options.

The first option is automatically selected.


```py
choice = view(box('Choose a color', mode='radio', options=[
    'blue', 'green', 'yellow', 'orange', 'red', 'black'
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/radio_basic.png)


## Set initial selection

Set `value=` to pre-select an option having that value.


```py
choice = view(box('Choose a color', mode='radio', value='yellow', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow'),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/radio_value.png)


## Mark options as selected

Set `selected=True` to pre-select an option.


```py
choice = view(box('Choose a color', mode='radio', options=[
    option('green', 'Green'),
    option('yellow', 'Yellow', selected=True),
    option('orange', 'Orange'),
    option('red', 'Red'),
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/radio_selected.png)


## Show pictorial options

Set `icon=` to show pictorial options.


```py
choice = view(box('Choose a chart type', mode='radio', options=[
    option('area', 'Area', icon='AreaChart', selected=True),
    option('bar', 'Bar', icon='BarChartHorizontal'),
    option('column', 'Column', icon='BarChartVertical'),
    option('line', 'Line', icon='LineChart'),
    option('scatter', 'Scatter', icon='ScatterChart'),
    option('donut', 'Donut', icon='DonutChart'),
]))
view(f'You chose {choice}.')
```


![Screenshot](assets/screenshots/radio_icon.png)
