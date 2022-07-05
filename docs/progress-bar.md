# Progress Bar

Use progress bars to show the completion status of long-running operations.

## Basic

Set `mode='progress'` to show a progress bar.


```py
view(box('Swapping time and space...', mode='progress'))
```


![Screenshot](assets/screenshots/progress_bar_basic.png)


## Set caption

Set `caption=` to show a caption below the bar


```py
view(box(
    'Swapping time and space',
    mode='progress',
    caption='Spinning violently around the y-axis...',
))
```


![Screenshot](assets/screenshots/progress_bar_caption.png)


## Set completion

Set `value=` to a number between `0` and `1` to show a completion status.


```py
view(box(
    'Swapping time and space',
    mode='progress',
    caption='Spinning violently around the y-axis...',
    value=0.75
))
```


![Screenshot](assets/screenshots/progress_bar_value.png)
