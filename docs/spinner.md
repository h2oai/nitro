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

Add `text-left`, `text-right`, `text-top` or `text-bottom` to the `mode` to align the text
to the `left`, `right`, `top`, or `bottom` of the spinner.


```py
view(
    col(
        'Default:',
        box('Reticulating splines...', mode='spinner'),
        'Left:',
        box('Reticulating splines...', mode='spinner text-left'),
        'Top:',
        box('Reticulating splines...', mode='spinner text-top'),
        'Right:',
        box('Reticulating splines...', mode='spinner text-right'),
        'Bottom:',
        box('Reticulating splines...', mode='spinner text-bottom'),
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
