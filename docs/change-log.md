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
