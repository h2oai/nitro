# Theming

Learn how to customize your app's color scheme.

## Set initial theme

To set the theme, set `theme=Theme(mode, accent)` when creating the app's `View()`.

`mode` sets the color scheme for prose, and `accent` sets the accent color for UI components.

- For light mode, set `mode` to one of `light` (default), `light gray`, `light slate`, `light zinc`, `light neutral`, or `light stone`.
- For dark mode, set `mode` to one of `dark` (default), `dark gray`, `dark slate`, `dark zinc`, `dark neutral`, or `dark stone`.

`light` is shorthand for `light gray`, and `dark` is shorthand for `dark gray`.
The colors `gray`, `slate`, `zinc`, `neutral`, and `stone` indicate the text color. The background color for dark mode is automatically chosen for you.

`accent` must be one of `red`, `orange`, `amber`, `yellow`, `lime`, `green`, `emerald`, `teal`, 
`cyan`, `sky`, `blue`, `indigo`, `violet`, `purple`, `fuchsia`, `pink`, `rose`, `slate`, `gray`, 
`zinc`, `neutral`, or `stone`.


```py
# App entry point
def main(view: View):
    pass

# Create theme
my_theme = Theme(
    mode='dark zinc',
    accent='indigo',
)

# Set theme when creating the View()
nitro = View(main, title='My App', caption='v1.0', theme=my_theme)

```



## Switch themes dynamically

Call `view.set(theme=Theme(...))` to change the theme dynamically.

The example below switches between light and dark modes.


```py
dark_mode = False
while True:
    response = view(
        box('Dark Mode', mode='toggle', value=dark_mode),
        # Sample text
        '## This is not a drill',
        lorem(5),
        # Sample fields
        box('Enter text', placeholder='Enter some text'),
        box('Enter a number', value=42),
        box('Check this', mode='check', value=True),
        box('Toggle this', mode='toggle', value=True),
        box('Are you sure?', mode='radio', options=['Yes', 'No']),
        box('Pick a flavor', mode='menu', options=['Chocolate', 'Vanilla'], value='Chocolate'),
        box('Pick a value', mode='range', value=42, range=(0, 100)),
        box('Pick a day', mode='day'),
        box('Rate this', mode='rating'),
        box(["Let's go!", 'Not now']),
        style='p-4'
    )
    dark_mode = response[0]
    view.set(theme=Theme(mode='dark' if dark_mode else 'light'))
```


![Screenshot](assets/screenshots/theme_dark_mode.png)


## Prose theme sampler

The example below shows all the prose theme variations.


```py
modes = [
    'light', 'dark',
    'light gray', 'light slate', 'light zinc', 'light neutral', 'light stone',
    'dark gray', 'dark slate', 'dark zinc', 'dark neutral', 'dark stone',
]

sample_text = f'## {lorem()}\n### {lorem()}\n{lorem(5)}\n### {lorem()}\n{lorem(5)}'

mode = modes[0]
while True:
    mode = view(
        box('Mode', mode='menu', options=modes, value=mode, live=True),
        sample_text,
        style='p-4'
    )
    view.set(theme=Theme(mode=mode))
```


![Screenshot](assets/screenshots/theme_prose_modes.png)


## Use color variables

*Color variables* are pre-defined, named colors that match the app's theme.

Color variables take the form `var(--name)`, or simply `$name`. For example, you can use
`var(--red)` or `$red` instead of hard-coded colors like `red` or `#ff0000` or `rgb(255,0,0)`.

Color variables can be passed wherever colors are accepted, like `background=`, `border=`, `color=`, and so on.

There are 16 pre-defined *spectrum colors*, derived automatically from the theme's accent color by matching its
saturation and lightness. Spectrum colors are useful for data visualizations and infographics. The naming of each
color is only indicative, and its hue might appear off depending on the position of the accent color's hue along the
color spectrum. For example, `$red` could appear pink or orange!

Additionally, there are pre-defined color variables for various *tones* of the theme's foreground (`$foreground`),
background (`$background`) and accent (`$accent`) colors.
Accent tones are prefixed with `$accent-`, and neutral tones (grays) are prefixed with `$neutral-`.


```py
style = dict(width=30, height=30, border='#777', margin='0 0 2.5rem 0')
view(
    '### Spectrum Colors',
    row(
        box(background='$red', **style),
        box(background='$lava', **style),
        box(background='$orange', **style),
        box(background='$amber', **style),
        box(background='$yellow', **style),
        box(background='$lime', **style),
        box(background='$mint', **style),
        box(background='$green', **style),
        box(background='$teal', **style),
        box(background='$cyan', **style),
        box(background='$sky', **style),
        box(background='$blue', **style),
        box(background='$indigo', **style),
        box(background='$purple', **style),
        box(background='$violet', **style),
        box(background='$pink', **style),
        wrap='normal',
    ),
    '### Theme Colors',
    row(
        box(background='$foreground', **style),
        box(background='$background', **style),
        box(background='$accent', **style),
        wrap='normal',
    ),
    '### Accent Tones',
    row(
        box(background='$accent-darker', **style),
        box(background='$accent-dark', **style),
        box(background='$accent-dark-alt', **style),
        box(background='$accent-primary', **style),
        box(background='$accent-secondary', **style),
        box(background='$accent-tertiary', **style),
        box(background='$accent-light', **style),
        box(background='$accent-lighter', **style),
        box(background='$accent-lighter-alt', **style),
        wrap='normal',
    ),
    '### Neutral Tones',
    row(
        box(background='$neutral-dark', **style),
        box(background='$neutral-primary', **style),
        box(background='$neutral-primary-alt', **style),
        box(background='$neutral-secondary', **style),
        box(background='$neutral-secondary-alt', **style),
        box(background='$neutral-tertiary', **style),
        box(background='$neutral-tertiary-alt', **style),
        box(background='$neutral-quaternary', **style),
        box(background='$neutral-quaternary-alt', **style),
        box(background='$neutral-light', **style),
        box(background='$neutral-lighter', **style),
        box(background='$neutral-lighter-alt', **style),
        wrap='normal',
    ),
)
```


![Screenshot](assets/screenshots/theme_colors.png)


## Some sample themes

This example provides some sample themes that you can use in your own app.


```py
themes = [
    Theme(
        background_color='#fff',
        foreground_color='#3e3f4a',
        accent_color='#ef5350',
    ),
    Theme(
        background_color='#fff',
        foreground_color='#3e3f4a',
        accent_color='#ec407a',
    ),
    Theme(
        background_color='#fff',
        foreground_color='#3e3f4a',
        accent_color='#ab47bc',
    ),
    Theme(
        background_color='#fff',
        foreground_color='#3e3f4a',
        accent_color='#7e57c2',
    ),
    Theme(
        background_color='#fff',
        foreground_color='#3e3f4a',
        accent_color='#5c6bc0',
    ),
    Theme(
        background_color='#fff',
        foreground_color='#3e3f4a',
        accent_color='#42a5f5',
    ),
    Theme(
        background_color='#3e3f4a',
        foreground_color='#fff',
        accent_color='#29b6f6',
    ),
    Theme(
        background_color='#3e3f4a',
        foreground_color='#fff',
        accent_color='#26c6da',
    ),
    Theme(
        background_color='#fff',
        foreground_color='#3e3f4a',
        accent_color='#26a69a',
    ),
    Theme(
        background_color='#fff',
        foreground_color='#3e3f4a',
        accent_color='#66bb6a',
    ),
    Theme(
        background_color='#3e3f4a',
        foreground_color='#fff',
        accent_color='#9ccc65',
    ),
    Theme(
        background_color='#3e3f4a',
        foreground_color='#fff',
        accent_color='#d4e157',
    ),
    Theme(
        background_color='#3e3f4a',
        foreground_color='#fff',
        accent_color='#ffee58',
    ),
    Theme(
        background_color='#3e3f4a',
        foreground_color='#fff',
        accent_color='#ffca28',
    ),
    Theme(
        background_color='#3e3f4a',
        foreground_color='#fff',
        accent_color='#ffa726',
    ),
    Theme(
        background_color='#fff',
        foreground_color='#3e3f4a',
        accent_color='#ff7043',
    ),
]

theme_lookup = {theme.accent_color: theme for theme in themes}
theme_names = list(theme_lookup.keys())
theme_names.sort()
theme_name = theme_names[0]

while True:
    response = view(
        box('Pick a theme', mode='color', value=theme_name, options=theme_names, live=True),
        col(
            # Sample fields
            box('Enter text', placeholder='Enter some text'),
            box('Enter a number', value=42),
            box('Check this', mode='check', value=True),
            box('Toggle this', mode='toggle', value=True),
            box('Are you sure?', mode='radio', options=['Yes', 'No']),
            box('Pick a flavor', mode='menu', options=['Chocolate', 'Vanilla'], value='Chocolate'),
            box('Pick a value', mode='range', value=42, range=(0, 100)),
            box('Pick a day', mode='day'),
            box('Rate this', mode='rating'),
            box(["Let's go!", 'Not now'])
        ),
    )
    theme_name = response[0]
    view.set(theme=theme_lookup.get(theme_name))
```


![Screenshot](assets/screenshots/theme_samples.png)
