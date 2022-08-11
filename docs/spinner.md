# Spinner

Use a spinner to indicate that a long-running operation is in progress,
and it's unsure how long it will take to complete.

## Basic

Call `box()` with `mode='spinner'` to show a spinner.


```py
view(box('Reticulating splines...', mode='spinner'))
```


![Screenshot](assets/screenshots/spinner_basic.png)


## Set alignment

Add `left`, `right`, `top` or `bottom` to the `mode` to set spinner position relative to the label.
The default is `top`.


```py
view(
    col(
        'Default:',
        box('Reticulating splines...', mode='spinner'),
        'Left:',
        box('Reticulating splines...', mode='left spinner'),
        'Top:',
        box('Reticulating splines...', mode='top spinner'),
        'Right:',
        box('Reticulating splines...', mode='right spinner'),
        'Bottom:',
        box('Reticulating splines...', mode='bottom spinner'),
    )
)
```


![Screenshot](assets/screenshots/spinner_align.png)


## Remove text

To display a spinner without text, don't pass any text to `box()`.


```py
view(box(mode='spinner'))
```


![Screenshot](assets/screenshots/spinner_only.png)
