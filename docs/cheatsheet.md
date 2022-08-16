# Cheatsheet

## Boxes

| Output                                                      | Code                                                                                                        |
|-------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| Show markdown.                                              | `'text'` <br> `box('text')` <br> `box('text', mode='md')`                                                   |
| Show styled box.                                            | `box(style='...')`                                                                                          |
| Show styled box with text.                                  | `box('text', style='...')`                                                                                  |
| Stack boxes vertically.                                     | `box(box(...), box(...), ...)`                                                                              |
| Stack boxes horizontally (with gaps).                       | `row(box(...), box(...), ...)` <br> `box(..., mode='row')`                                                  |
| Stack boxes vertically (with gaps).                         | `col(box(...), box(...), ...)` <br> `box(..., mode='col')`                                                  |
| Show boxes in a group (collapsible).                        | `box(..., title='Group1')`                                                                                  |
| Show tabs.                                                  | `row(group1, group1, ...)` <br> `row(box(..., title='Group1'), box(..., title='Group2'), ...)`              |
| Show vertical tabs.                                         | `col(group1, group2, ...)` <br> `col(box(..., title='Group1'), box(..., title='Group2'), ...)`              |
| Show a textbox.                                             | `box('Label', value='Alice')` <br> `box('Label', mode='text')`                                              |
| Show a spinbox.                                             | `box('Label', value=42)` <br> `box('Label', mode='number')`                                                 |
| Show a checkbox.                                            | `box('Label', value=False)` <br> `box('Label', value=True)` <br> `box('Label', mode='check')`               |
| Show a toggle.                                              | `box('Label', mode='toggle')` <br> `box('Label', mode='toggle', value=True)`                                |
| Show a checklist.                                           | `box('Label', mode='check', options=[...])`                                                                 |
| Show buttons stacked horizontally.                          | `box([...])` <br> `box(mode='button', options=[...])`                                                       |
| Show buttons stacked vertically.                            | `box([...], mode='vertical button')` <br> `box(mode='vertical button', options=[...])`                      |
| Show buttons with captions (compound buttons).              | `box(mode='button', options=[option(..., caption='...'), ...])`                                             |
| Show buttons with menus (split buttons).                    | `box(mode='button', options=[option(..., options=[...]), ...])`                                             |
| Show radio buttons.                                         | `box('Label', mode='radio', options=[...])`                                                                 |
| Show a dropdown menu (single-select).                       | `box('Label', mode='menu', options=[...])`                                                                  |
| Show a dropdown menu (multi-select).                        | `box('Label', mode='multi menu', options=[...])`                                                            |
| Show a dropdown menu with arbitrary text input (combo box). | `box('Label', mode='editable menu', options=[...])`                                                         |
| Show a dropdown menu with grouped options.                  | `box('Label', mode='menu', options=[option(..., options=[...]), ...])`                                      |
| Show a slider.                                              | `box('Label', mode='range')`                                                                                |
| Show a range slider.                                        | `box('Label', mode='range', value=(min, max))`                                                              |
| Show a time picker.                                         | `box('Label', mode='time')`                                                                                 |
| Show a date picker.                                         | `box('Label', mode='date')`                                                                                 |
| Show a week picker.                                         | `box('Label', mode='week')`                                                                                 |
| Show a month picker.                                        | `box('Label', mode='month')`                                                                                |
| Show a calendar.                                            | `box('Label', mode='day')`                                                                                  |
| Show a tag picker.                                          | `box('Label', mode='tag', options=[...])`                                                                   |
| Show a color picker.                                        | `box('Label', mode='color')`                                                                                |
| Show a color palette.                                       | `box('Label', mode='color', options=[...])`                                                                 |
| Show a star-rating.                                         | `box('Label', mode='rating')`                                                                               |
| Show a file uploader.                                       | `box('Label', mode='file')`                                                                                 |
| Show a multiple file uploader.                              | `box('Label', mode='multi file')`                                                                           |
| Show a indeterminate progress bar.                          | `box('Label', mode='progress')` <br> `box('Label', mode='progress', caption='...')`                         |
| Show a progress bar.                                        | `box('Label', mode='progress', value=0.42)` <br> `box('Label', mode='progress', caption='...', value=0.42)` |
| Show a spinner.                                             | `box('Label', mode='spinner')`                                                                              |
| Show a separator.                                           | `box('Label', mode='separator')`                                                                            |
| Show a vertical separator.                                  | `box('Label', mode='vertical separator')`                                                                   |
| Show an image.                                              | `box(image='...')`                                                                                          |
| Show a web view (`iframe`).                                 | `box(mode='web', path='...')`                                                                               |
| Show a table                                                | `box(mode='table', headers=[...], options=[option(..., options=[...]), ...])`                               |
| Show a table with selectable rows (multi-select).           | `box(mode='multi table', headers=[...], options=[option(..., options=[...]), ...])`                         |
| Show a table with selectable rows (single-select).          | `box(mode='selectable table', headers=[...], options=[option(..., options=[...]), ...])`                    |
| Show a table with grouped rows.                             | `box(mode='table', headers=[...], options=[option(..., options=[option(..., options=[...]), ...]), ...])`   |
| Make a column's cells clickable.                            | `header(..., mode='link'`                                                                                   |
| Render markdown in a column's cells.                        | `header(..., mode='md')`                                                                                    |
| Pass options                                                | `box(..., options=[option('red', 'Red'), ...])` <br> `box([option('red', 'Red'), ...], ...)`                |
| Pass options using pairs                                    | `box(..., options=[('red', 'Red'), ('blue', 'Blue')])` <br> `box([('red', 'Red'), ('blue', 'Blue')], ...)`  |
| Pass options using tuple                                    | `box(..., options=('red', 'blue'))`                                                                         |
| Pass options using list                                     | `box(..., options=['red', 'blue'])` <br> `box(['red', 'blue'], ...)`                                        |
| Pass options using dict                                     | `box(..., options=dict(red='Red', blue='Blue'))`                                                            |
| Pass options using string                                   | `box(..., options='red blue')`                                                                              |

## Views

| Operation                                     | Code                                 |
|-----------------------------------------------|--------------------------------------|
| Overwrite current view                        | `view(...)`                          |
| Overwrite boxes inside box `'foo'`.           | `view(..., at='foo *')`              |
| Overwrite boxes starting at box `'foo'`.      | `view(..., at='foo')`                |
| Overwrite boxes before box `'foo'`.           | `view(..., at=':foo')`               |
| Overwrite boxes after box `'foo'`.            | `view(..., at='foo:')`               |
| Add boxes to current view.                    | `view.add(...)`                      |
| Add boxes inside box `'foo'`.                 | `view.add(..., at='foo *')`          |
| Add boxes before box `'foo'`.                 | `view.add(..., at=':foo')`           |
| Add boxes after box `'foo'`.                  | `view.add(..., at='foo:')`           |
| Clear current view.                           | `view.clear()`                       |
| Clear boxes inside box `'foo'`.               | `view.clear(at='foo *')`             |
| Clear boxes starting at box `'foo'`.          | `view.clear(at='foo')`               |
| Clear boxes before box `'foo'`.               | `view.clear(at=':foo')`              |
| Clear boxes after box `'foo'`.                | `view.clear(at='foo:')`              |
| Show view, but without the "Continue" button. | `view(..., halt=True)`               |
| Show view, but don't wait for inputs.         | `view(..., read=False)`              |
| Show view, but in a popup.                    | `view(..., popup=True, title='...')` |
| Set view title.                               | `view.set(title='...')`              |
| Set view caption.                             | `view.set(caption='...')`            |
| Set view menu.                                | `view.set(menu='...')`               |
| Set view nav.                                 | `view.set(nav='...')`                |
| Set view theme.                               | `view.set(theme='...')`              |
| Jump to another view function.                | `view.jump(func)`                    |
| Launch external URL.                          | `view.jump(url)`                     |
| Launch external URL in a popup.               | `view.jump(url, popup=1)`            |
| Navigate to another URL.                      | `view.jump(url, target='_self')`     |

