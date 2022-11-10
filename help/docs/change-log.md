---
template: overrides/main.html
---

# Change Log

## Background

### Versioning

H2O Nitro follows [Semantic Versioning](https://semver.org/). Minor and patch releases should never contain breaking
changes.

When referencing the [`h2o-nitro` package](https://pypi.org/project/h2o-nitro/) from your `requirements.txt`
or `setup.py`, you should always use a version constraint such as `>=4.2, <5` (any version 4.2 or greater, but less than
5), since major releases of H2O Nitro do include breaking changes.

### Support Policy

For LTS releases, bug fixes are provided for 2 years and security fixes are provided for 3 years. These releases provide
the longest window of support and maintenance. For general releases, bug fixes are provided for 6 months and security
fixes are provided for 1 year.

## v0.18.0

Nov 10, 2022

- Added
    - Data graphics primitives (point, line, curve, bar, rect, polygon, etc.)

## v0.17.0

Oct 18, 2022

- Added
    - Relative time formatting (N days ago, in N days, yesterday, today, tomorrow).
    - Allow customizing how client locale is interpreted (`locale=`).
    - Disabled state for all widgets and buttons (`box(disabled=True)` and `option(disabled=True)`).
    - Set `data-name` HTML attribute for all boxes where a `name=` is supplied (for test automation).
    - Always show tooltips on table column headers.
- Fixed
    - Mode `multi live menu` doesn't block UI when changed.

## v0.16.3

Sep 27, 2022

- Fixed
    - Hang when internal `jump()` is called after an external `jump()`.
    - Misaligned compound button when it contains a submenu.

## v0.16.2

Sep 22, 2022

- Added
    - Capture and display unhandled Python exceptions with stack trace.
    - Ignore input messages in case of race during switch.
- Fixed
    - Help panel doesn't update if a different info icon is clicked

## v0.16.1

Sep 08, 2022

- Fixed
    - `view.jump()` to bare urls redirects to quoted hash.
    - Revert intermediate exception handling until a permanent solution is in place.

## v0.16.0

Sep 07, 2022

- Added
    - Format strings (templates) with support for primitives, arrays, and nested objects.
    - Locale-sensitive number formatting (decimal, percent, scientific, engineering, compact, currency, accounting, units and numbering systems).
    - Locale-sensitive date and time formatting (styles, components, calendars, time zones, eras, periods, numbering systems).
    - Locale-sensitive list formatting (lists, conjunctions, disjunctions).
    - Block-specific locales (for multilingual user interfaces).
    - Generic clickable inputs (`mode='input'` and `mode='tap'`).
    - Keyboard shortcuts (`box(hotkey=...)`) for individual boxes, top level menu and nav.
    - Allow view functions to accept arbitrary parameters.
    - `link()` API to conjure internal links.
    - `box(link=...)` can be set to functions in addition to strings.
- Changed
    - `box(path=...)` renamed to `box(link=...)` for consistency with `link()` API.
    - Always launch external URLs in a new window.

## v0.15.0

Aug 23, 2022

- Added
    - Support for special variables in Nitrogen headers that refer to current file, dir, etc.
    - Simulation mode (`-source`) to test `nitro run` locally.
- Changed
    - Remove deprecated `FLASK_ENV` from all Flask examples; use `--debug` instead.

## v0.14.2

Aug 19, 2022

- Fixed
    - Unblock app when external URLs are launched.
    - Make `view.jump(func)` work via hashbangs.
    - Make `view.jump(popup=True)` consistent with `view(popup=True)`.

## v0.14.1

Aug 18, 2022

- Changed
    - Show empty indicator in checklists when empty.
    - `box(..., path='...')` now behaves the same as `view.jump()`.
    - `path=` links requires `#!` prefixes to jump to other functions.
    - `view.jump()` allows jumping to relative paths.
- Fixed
    - `check` mode shows checkbox instead of checklist when options are empty.
    - `menu` and `date` modes active/hover mode color contrasts are too low.

## v0.14.0

Aug 15, 2022

**Warning: This release has several breaking changes.**

The major focus for this release was to support arbitrary styles for boxes, and reducing the code clutter typically
associated with mixing presentation and behavioral logic.

- Added
    - Support for applying arbitrary styles using [Tailwind](https://tailwindcss.com/) notation. Note that Nitro does
      not use the official Tailwind library, but includes an entirely custom incremental compiler that expands and
      applies styles on the fly.
    - Concise styling notation: `box(...) / style` is equivalent to `box(..., style='')`.
    - Extensible styles: `box(...) / a / b` is shorthand for `box(..., style=f'{a} {b}')`.
    - Extensible boxes: `box(x, y)(p, q)` clones a box and puts `p` and `q` in it.
    - Support for rendering SVG graphics.
    - Dozens of examples for custom components like cards, stats, pagination, etc. built using pure Python.
- Changed
    - Typography and color handling have been completely overhauled.
    - Markdown styling has been completely overhauled. Now uses Tailwind's `prose` styles.
    - `box(style=)` now controls how a box looks, and replaces individual settings like `tile`, `width`, `color`, and so
      on.
      A box can have several styles, e.g. `box(style='p-4 grow text-blue-500'`).
    - `box(mode=)` controls how a box behaves, and replaces individual flags like `multiple`, `required`, and so on. A
      box
      can have several modes, e.g. `box(mode='required multi menu')`.
    - `view(insert=, remove=, inside=, before=, at=, after=)` replaced with `view.add(at=)`, `view.clear(at=)`.
    - `box([options...])` now can be used to create any picker that accepts options, not just buttons.
    - Themes have been simplified. Instead of specifying background, foreground and accent colors, you only need to
      specify
      light/dark modes and an accent color.
    - `view.jump()` opens URLs in a new window (instead of the current window).
    - `view.jump(target='_self')` opens URLs in the current window.
    - `box(title=)` is now interpreted as a collapsible group.
    - `row(box(title=), ...)` is now interpreted as a tabbed view.
    - `col(box(title=), ...)` is now interpreted as a vertical tabbed view (not as an accordion view).
- Removed
    - `box(items=[a, b, c])` removed. Use `box(a, b, c)` instead, i.e. `box()` is now variadic.
    - `box(row=)` removed. Use `row()` or `col()` instead.
    - `box(layout='column')` removed. Use `mode='vertical'` instead.
    - `box(tile=)` removed. Use `style='justify-*'` instead.
    - `box(cross_tile=)` removed. Use `style='items-*'` instead.
    - `box(wrap=)` removed. Use `style='flex-wrap'` instead.
    - `box(gap=)` removed. Use `style='gap-*'` instead.
    - `box(grow=)` removed. Use `style='grow'` instead.
    - `box(shrink=)` removed. Use `style='shrink'` instead.
    - `box(basis=)` removed. Use `style='basis-*'` instead.
    - `box(align=)` removed. Use `style='text-*'` instead.
    - `box(width=)` removed. Use `style='w-*'` instead.
    - `box(height=)` removed. Use `style='h-*'` instead.
    - `box(margin=)` removed. Use `style='m-*'` instead.
    - `box(padding=)` removed. Use `style='p-*'` instead.
    - `box(color=)` removed. Use `style='text-*'` instead.
    - `box(background=)` removed. Use `style='bg-*'` instead.
    - `box(border=)` removed. Use `style='border-*'` instead.
    - `box(fit=)` removed. Use `style='object-*'` instead.
    - `box(multiple=)` removed. Use `mode='multi'` instead.
    - `box(required=)` removed. Use `mode='required'` instead.
    - `box(password=)` removed. Use `mode=''password` instead.
    - `box(editable=)` removed. Use `mode=''editable` instead.
    - `box(live=)` removed. Use `mode='live'` instead.
    - `header(width=)` removed. Use `style='min-w-* max-w-*'` instead.
    - `header(resizable=)` removed. Use `mode='fixed'` instead.
    - `header(multiline=)` removed. Use `mode='multiline'` instead.
    - `view(before='foo')` removed. Use `view(at=':foo')` instead.
    - `view(after='foo')` removed. Use `view(at='foo:')` instead.
    - `view(inside='foo')` removed. Use `view(at='foo *')` instead.
    - `view(insert=True)` removed. Use `view.add()` instead.
    - `view(insert=True, at='foo')` removed. Use `view.add(at='foo')` instead.
    - `view(insert=True, before='foo')` removed. Use `view.add(at=':foo')` instead.
    - `view(insert=True, after='foo')` removed. Use `view.add(at='foo:')` instead.
    - `view(insert=True, inside='foo')` removed. Use `view.add(at='foo *')` instead.
    - `view(remove=True)` removed. Use `view.clear()` instead.
    - `view(remove=True, at='foo')` removed. Use `view.clear(at='foo')` instead.
    - `view(remove=True, before='foo')` removed. Use `view.clear(at=':foo')` instead.
    - `view(remove=True, after='foo')` removed. Use `view.clear(at='foo:')` instead.
    - `view(remove=True, inside='foo')` removed. Use `view.clear(at='foo *')` instead.
    - `box(mode='tabs')` removed. Use `row(box(title=), ...)` instead.

## v0.13.2

Jul 22, 2022

- Fixed
    - Clear any stale / uncommitted state in front-end on `view.jump()`.

## v0.13.1

Jul 21, 2022

- Changed
    - `view.jump()` now performs an implicit socket read, which can help prevent infinite loops in
      situations where application code does not peform an explicit read after a jump.

## v0.13.0

Jul 16, 2022

- Added
    - `view.jump()` API for back-button handling and opening URLs in current, new, or popup windows.
    - Tabbed layout (`mode='tabs'`).
    - Expander component (vertical tabbed layout, with expandable section).
    - Set `hint=` to show context-sensitive popup hints on components.
    - Set `help=` to show context-sensitive long-form help about components.
    - (Experimental) Basic i18n/l10n support: load locale-specific string during init.
    - (Experimental) Use `@foo` wherever text is accepted to reference locale-specific strings.
    - Cheatsheet section in docs (https://nitro.h2o.ai/cheatsheet).
- Changed
    - Default font size of table component increased for improving readability.
    - Checkboxes for selectable tables are always displayed (instead of only on hover).
    - `box(row=False)` is marked obsolete. Use `box(layout='column')` instead.
- Fixed
    - Textboxes with masks don't display prefix, suffix, icon

## v0.12.0

Jul 05, 2022

- Added
    - Set `live=True` on any component except textboxes to handle changes immediately.
    - Banner component in six styles: info, success, warning, critical, blocked, and error.
    - Progress bar component with two styles: completion-status and indeterminate.
    - Spinner component (infinite) with customizable label alignment.
- Fixed
    - Client might return stale values if later sync does not overwrite previous values.
    - Selected date is not reflected in calendar.
    - Respect scalar initial value if table is in single-select mode.
    - Remove (harmless) xid mismatch errors when re-entering workflows.

## v0.11.0

Jun 27, 2022

**To upgrade:**

- Use `pip install "h2o-nitro[web]"` instead of `pip install h2o-nitro`.
- Change `from h2o_nitro import web_directory` to `from h2o_nitro_web import web_directory`.

**Why?**

The `h2o-nitro` package is now a smaller PyPI package (~13KB) designed to work
in both web assembly (Wasm) and regular Python environments.
The full `pip install "h2o-nitro[web]"` includes the UI assets required for developing web apps.

- Added
    - Apps now work entirely in-browser (via Pyodide).
    - Ability to host and execute browser-local Python via a Wasm web-worker.
    - Ability to execute Python code in a HTML file's script tag.
    - Ability to dynamically load and execute external Python modules.
    - Ability to dynamically load and copy external Python libraries.
    - Ability to dynamically install Pyodide and PyPI packages.
    - Starter bundles with examples for building HTML-based Nitro apps.
- Changed
    - Remove web assets from `h2o-nitro` PyPI package (~13KB).
    - Publish separate `h2o-nitro-web` PyPI package with web assets.
    - Remove android- and apple- icons from web assets.
    - Use a single CSS file for all user-customizable style rules.
- Fixed
    - Don't auto-grow a column's items automatically.
    - Front-end crash in older browsers caused by `String.replaceAll()`.

## v0.10.1

Jun 20, 2022

- Changed
    - Default color picker to null instead of black.
    - Submit scalar values for single-select tables, not lists.
- Fixed
    - Make dropdown, combobox, choice group, color picker always submit default values.

## v0.10.0

Jun 17, 2022

- Added
    - **Editing.** Append, insert, overwrite or remove parts of the UI. Add selector syntax.
    - **Chromeless mode.** Append `?mode=chromeless` to URL. Removes header, menu and nav.
    - Automatically block/unblock UI when request is being processed.
    - New webview (iframe) component (use boxes with `mode='web'`).
    - Launch menu and nav workflows using `#!` location hashes.
    - Specify additional `#!` location hashes via view `routes`.
    - Disable automatic continue button by passing `halt=True` to `view()`.
    - Add previous/next buttons to each page in livedocs.
    - Improve communication / message exchange robustness and error reporting.
- Changed
    - Default app caption to package version.
    - Improve checklist item spacing.
    - Display livedocs examples in webviews. Improved interactivity.
- Fixed
    - Don't submit values from non-interactive components.
    - Show automatic continue button if table is set to single- or multi- select mode.
    - Grow non-rows inside containers to fit width.

## v0.9.2

Jun 09, 2022

- Fixed
    - Don't return values for non-interactive components (separator, image, plots)

## v0.9.1

Jun 09, 2022

- Fixed
    - Wonky markdown list rendering when there is trailing whitespace on line immediately following list.
    - Respect column width on tables when scalar.

## v0.9.0

Jun 07, 2022

- Added
    - `nitro` command line program, shipped separately from Python wheel.
    - `nitro run` command to download, set up, and run any Nitro app hosted on the world wide web.
    - `nitro clone` command to download and set up Nitro apps.
- Fixed
    - Don't overflow box contents if `width` or `height` is set.
- Removed
    - Python-based CLI (`nitro create`, `nitro list`, `nitro docs` superceded by `nitro run`).

## v0.8.4

Jun 01, 2022

- Fixed
    - Wrap code blocks properly when lang is not provided.

## v0.8.3

May 30, 2022

- Changed
    - (Perf) Load a plugin's scripts sequentially; load plugins in parallel.

## v0.8.2

May 26, 2022

- Added
    - Plugin / extension mechanism for loading and using third-party front-end/back-end libraries.

## v0.7.1

May 23, 2022

- Changed
    - Import static assets relative to `index.html` instead of `/`.

## v0.7.0

May 15, 2022

- Added
    - Support for modal dialogs. Use `view(popup=True)` to pop-up content using a dialog.
    - File upload component (`box mode='file'`) with support for multiple file uploads and progress tracking.

## v0.6.0

Apr 28, 2022

- Added
    - Table component (`box mode='table'`) with selectable rows, grouping, sorting, column resizing, and markdown
      support.

- Fixed
    - Don't show automatic *Continue* button if a toggle is present on the page.

## v0.5.0

Apr 21, 2022

**Highlights**: Major improvements to typography; support for theming.

- Added
    - Theming: specify startup theme, switch themes dynamically, dark-mode, define custom themes.
    - Auto-generated matching colors for data visualizations.
    - Support for using color variables wherever colors are supported, e.g. `$red`.
    - Customize app's CSS by editing `styles.css`.
    - Toggle component (`box mode='toggle'`).
    - Image component (`box mode='image'`), with support for different kinds of `fit`.
    - Standalone checkboxes (`box mode='check'` without options).
    - Docs pages now include screenshots for each example.
    - Allow using images for box/row/col backgrounds.
    - Improve connection, disconnection, error overlays.
    - Basic lorem-ipsum placeholder text generator, helpful for mockups.
    - The box/row/col `name` is translated to the HTML `data-name` attribute for automation.
    - Add an advanced layout example. More to come in future versions!

- Changed
    - Major improvements to typography and layout
    - Default to *Roboto Slab*, a friendlier-looking, geometric slab-serif font.
    - Automatically render first button in a set as the primary button.
    - Automatically mark first radio button in a set as selected.
    - Automatically render a checkbox if box value is a boolean.

- Fixed
    - Bug: Dropdown does not display selected value when changed.
    - Respect `align=` for horizontal button sets.

## v0.4.2

Apr 01, 2022

- Fixed
    - Fix Flask error 'PosixPath' object has no attribute 'rstrip' in Python < 3.8

## v0.4.1

Apr 01, 2022

Nitro is open source. April Fools'. Not.

## v0.3.0

Mar 31, 2022

- Added
    - Add `recruitment` starter app template for use with `nitro create`.
    - Bundle all Fluent icons with release.

## v0.2.0

Mar 30, 2022

- Added
    - Run `nitro create` to create a new app using Flask, Tornado or Starlette.
    - Run `nitro docs` to launch the built-in interactive tour and documentation.
- Changed
    - `box()` defaults to text blocks instead of textboxes.

## v0.1.0

Mar 29, 2022

- Initial version
