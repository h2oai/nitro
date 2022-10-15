---
template: overrides/main.html
---
# Localization

Nitro includes comprehensive support for internationalization and localization, including:

- Locale detection.
- Translation dictionaries.
- Locale-specific number, currency, units, accounting, date, time, relative time, and list formatting.
- Alternative numbering and calendar systems.
- Multi-lingual screens: use different languages on different parts of the same screen.

## Basics

To add support for additional languages, make two changes to your app:

1. Pass resource dictionaries to `View()` for each language.
2. Reference strings using `@` instead of hard-coding them.

Before:

```py
def main(view: View):
    view(box('Hello, world!'))
    
nitro = View(main)
```

After:

```py
def main(view: View):
    view(box('@hello')) # Reference key @hello instead.

nitro = View(
    main,
    resources={
        'en-US': dict(
            hello='Hello, world!'
        ),
        'es-ES': dict(
            hello='Hola Mundo!'
        ),
    },
)
```

The above example will display 'Hola Mundo!' when the client locale is set to `es-ES`.

By default, Nitro will detect the user's locale and display the corresponding translations.
To change this behavior, you can either enforce the default locale, or provide rules to handle the locale.

## Disable locale detection

To disable automatic locale detection, pass `locale=`:

```py
nitro = View(
    main,
    resources={
        'en-US': dict(
            hello='Hello, world!'
        ),
        'es-ES': dict(
            hello='Hola Mundo!'
        ),
    },
    locale='en-US' # Always show English regardless of client locale.
)
```

## Customize locale handling

To dynamically handle the client's locale and provide alternatives, pass a callback function instead of a locale string.

```py

def _handle_locale(locale: str) -> str:
    # Show US English for any English locale.
    if locale.startswith('en'):
        return 'en-US'
    
    # Show Spanish otherwise
    return 'es-ES'

nitro = View(
    main,
    resources={
        'en-US': dict(
            hello='Hello, world!'
        ),
        'es-ES': dict(
            hello='Hola Mundo!'
        ),
    },
    locale=_handle_locale # Pass a callback function
)
```

## Locale-specific formatting

`@` strings can reference `=` strings to perform locale-specific formatting.

Before:

```py
def main(view: View):
    view(box('=Donuts sold: {donuts num}', data=dict(donuts=123456.789))) 
    
nitro = View(main)
```

After:

```py
def main(view: View):
    view(box('@sold', data=dict(donuts=123456.789))) 

nitro = View(
    main,
    resources={
        'en-US': dict(
            sold='=Donuts sold: {donuts num}'
        ),
        'es-ES': dict(
            sold='=Donas vendidas: {donuts num}'
        ),
    },
)
```

See:

- [Formatting basics](../guide/format.md)
- [Formatting numbers](../guide/format-numbers.md)
- [Formatting dates](../guide/format-dates.md)
