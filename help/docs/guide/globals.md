---
template: overrides/main.html
---
# Globals

Configure top-level menu, navigation and hotkeys.

## Hotkeys

Set `hotkeys=` to configure keyboard shortcuts.

Examples:
- `option(cut, 'x')` calls the function `cut()` when `x` is pressed.
- `option(cut, 'ctrl+x')` calls the function `cut()` when `control` and `x` are pressed together.
- `option(cut, 'ctrl+shift+x')` calls the function `cut()` when `control`, `shift` and `x` are pressed together.
- `option(cut, 'ctrl+x, command+x')` calls the function `cut()` when either `ctrl+x` or `command+x` are pressed.

Supported modifiers: `shift`, `option`, `alt`, `ctrl`, `control`, `command`.

Supported special keys: `backspace`, `tab`, `clear`, `enter`, `return`, `esc`, `escape`, `space`, `up`, `down`,
`left`, `right`, `home`, `end`, `pageup`, `pagedown`, `del`, `delete`, `f1` - `f19`, `num_0` - `num_9`,
`num_multiply`, `num_add`, `num_enter`, `num_subtract`, `num_decimal`, `num_divide`.


```py
# Hotkey handler for Cut (ctrl+x)
def cut(view: View):
    print('Cut!')

# Hotkey handler for Copy (ctrl+c)
def copy(view: View):
    print('Copy!')

# Hotkey handler for Paste (ctrl+v)
def paste(view: View):
    print('Paste!')

# App entry point
def main(view: View):
    pass

# Pass hotkeys= to register hotkey handlers
nitro = View(main, title='My App', caption='v1.0', hotkeys=[
    option(cut, 'ctrl+x'),
    option(copy, 'ctrl+c'),
    option(paste, 'ctrl+v'),
])

```

