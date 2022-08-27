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
style = 'text-white rounded-full px-5 py-2.5 text-center mr-2 mb-2 '
color = view(
    'This is your last chance. After this, there is no turning back.',
    row(
        box(
            'Press Alt+b to take the blue pill',
            mode='tap', value='blue', hotkey='alt+b'
        ) / (style + 'bg-blue-700 hover:bg-blue-800'),
        box(
            'Press Alt+r to take the red pill',
            mode='tap', value='red', hotkey='alt+r'
        ) / (style + 'bg-red-700 hover:bg-red-800'),
        mode='input',
        ),
)
view(f'You took the {color} pill!')
```


![Screenshot](assets/screenshots/hotkey_tap.png)
