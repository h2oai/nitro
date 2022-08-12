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
| Show boxes in tabs.                                         | `row(box(..., title='Label1'), box(..., title='Label2'), ...)`                                              |
| Show boxes in vertical tabs.                                | `col(box(..., title='Label1'), box(..., title='Label2'), ...)`                                              |
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

## Views

| Operation                                     | Code                                       |
|-----------------------------------------------|--------------------------------------------|
| Overwrite current view                        | `view(...)`                                |
| Overwrite boxes inside box `'foo'`.           | `view(..., inside='foo')`                  |
| Overwrite boxes starting at box `'foo'`.      | `view(..., at='foo')`                      |
| Overwrite boxes before box `'foo'`.           | `view(..., before='foo')`                  |
| Overwrite boxes after box `'foo'`.            | `view(..., after='foo')`                   |
| Append boxes to current view.                 | `view(..., insert=True)`                   |
| Append boxes inside box `'foo'`.              | `view(..., insert=True, inside='foo')`     |
| Insert boxes before box `'foo'`.              | `view(..., insert=True, before='foo')`     |
| Insert boxes after box `'foo'`.               | `view(..., insert=True, after='foo')`      |
| Clear current view.                           | `view(remove=True)`                        |
| Remove boxes inside box `'foo'`.              | `view(remove=True, inside='foo')`          |
| Remove boxes starting at box `'foo'`.         | `view(remove=True, at='foo')`              |
| Remove boxes before box `'foo'`.              | `view(remove=True, before='foo')`          |
| Remove boxes after box `'foo'`.               | `view(remove=True, after='foo')`           |
| Show view, but without the "Continue" button. | `view(..., halt=True)`                     |
| Show view, but don't wait for inputs.         | `view(..., read=False)`                    |
| Show view, but in a popup.                    | `view(..., popup=True, title='...')`       |
| Set view title.                               | `view.set(title='...')`                    |
| Set view caption.                             | `view.set(caption='...')`                  |
| Set view menu.                                | `view.set(menu='...')`                     |
| Set view nav.                                 | `view.set(nav='...')`                      |
| Set view theme.                               | `view.set(theme='...')`                    |
| Jump to another view function.                | `view.jump(func)`                          |
| Jump to another URL.                          | `view.jump(url)`                           |
| Jump to another URL in a new window.          | `view.jump(url, target='_blank')`          |
| Jump to another URL in a new popup window.    | `view.jump(url, target='_blank', popup=1)` |

