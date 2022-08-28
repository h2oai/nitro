---
template: overrides/main.html
---
# Hotkeys

Assign keyboard shortcuts to actions.

## Tap

Set `hotkey=` to assign a keyboard shortcut to a `tap` `input` box.

Examples:
- `hotkey='x'`: `x` is pressed.
- `hotkey='ctrl+x'`:  `control` and `x` are pressed together.
- `hotkey='ctrl+shift+x'`: `control`, `shift` and `x` are pressed together.
- `hotkey='ctrl+x, command+x'`: either `ctrl+x` or `command+x` are pressed.

Supported modifiers: `shift`, `option`, `alt`, `ctrl`, `control`, `command`.

Supported special keys: `backspace`, `tab`, `clear`, `enter`, `return`, `esc`, `escape`, `space`, `up`, `down`,
`left`, `right`, `home`, `end`, `pageup`, `pagedown`, `del`, `delete`, `f1` - `f19`, `num_0` - `num_9`,
`num_multiply`, `num_add`, `num_enter`, `num_subtract`, `num_decimal`, `num_divide`.


```py
def style(color):
    return f'text-white rounded-full px-5 py-2.5 text-center mr-2 mb-2 bg-{color}-700 hover:bg-{color}-800'

color = view(
    'This is your last chance. After this, there is no turning back.',
    row(
        box('Blue pill (alt+b)', mode='tap', value='blue', hotkey='alt+b') / style('blue'),
        box('Red pill (alt+r)', mode='tap', value='red', hotkey='alt+r') / style('red'),
        mode='input',
    ),
)
view(f'You took the {color} pill!')
```


![Screenshot](assets/screenshots/hotkey_tap.png)
