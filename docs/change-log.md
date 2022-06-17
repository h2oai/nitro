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
