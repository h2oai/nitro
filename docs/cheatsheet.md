# Cheatsheet

## Widgets

| Output | Code |
|--------|------|
| Render markdown. | `'text'` or `box('text')` or `box('text', mode='md')`  |
| Show a textbox. | `box('text', value='string')` or `box('text', mode='text')` |
| Show a spinbox. | `box('text', value=42)` or `box('text', mode='number')` |
| Show a checkbox. | `box('text', value=False)` or `box('text', value=True)` or `box('text', mode='check')` |
| Show a checklist. | `box('text', mode='check', options=[...])` |
| Show a toggle. | `box('text', mode='toggle')` |
| Show buttons stacked horizontally. | `box([...])` or `box(mode='button', options=[...])` |
| Show buttons stacked vertically. | `box([...], layout='column')` or `box(mode='button', layout='column', options=[...])` |
| Show buttons with captions (compound buttons). | `box(mode='button', options=[option(..., caption='...'), ...])` |
| Show buttons with menus (split buttons). | `box(mode='button', options=[option(..., options=[...]), ...])` |
| Show radio buttons. | `box('text', mode='radio', options=[...])` |
| Show a dropdown menu (single-select). | `box('text', mode='menu', options=[...])` |
| Show a dropdown menu (multi-select). | `box('text', mode='menu', options=[...], multiple=True)` |
| Show a dropdown menu with arbitrary text input (combo box). | `box('text', mode='menu', options=[...], editable=True)` |
| Show a dropdown menu with grouped options. | `box('text', mode='menu', options=[option(..., options=[...]), ...])` |
| Show a slider. | `box('text', mode='range')` |
| Show a range slider. | `box('text', mode='range', value=(min, max))` |
| Show a time picker. | `box('text', mode='time')` |
| Show a date picker. | `box('text', mode='date')` |
| Show a week picker. | `box('text', mode='week')` |
| Show a month picker. | `box('text', mode='month')` |
| Show a calendar. | `box('text', mode='day')` |
| Show a tag picker. | `box('text', mode='tag', options=[...])` |
| Show a color picker. | `box('text', mode='color')` |
| Show a color palette. | `box('text', mode='color', options=[...])` |
| Show a star-rating. | `box('text', mode='rating')` |
| Show a file uploader. | `box('text', mode='file')` |
| Show a file uploader (multiple files). | `box('text', mode='file', multiple=True)` |
| Show a indeterminate progress bar. | `box('text', mode='progress', caption='...')` |
| Show a progress bar. | `box('text', mode='progress', caption='...', value=x)` |
| Show a spinner. | `box('text', mode='spinner')` |
| Show a separator. | `box('text', mode='separator')` |
| Show an image. | `box(image='...')` |
| Show and scale an image. | `box(image='...', fit='...')` |
| Show a web view (`iframe`). | `box(mode='web', path='...')` |
| Show a table | `box(mode='table', headers=[...], options=[option(..., options=[...]), ...])` |
| Show a table with selectable rows (multi-select). | `box(mode='table', headers=[...], options=[option(..., options=[...]), ...], multiple=True)` |
| Show a table with selectable rows (single-select). | `box(mode='table', headers=[...], options=[option(..., options=[...]), ...], multiple=False)` |
| Show a table with grouped rows. | `box(mode='table', headers=[...], options=[option(..., options=[option(..., options=[...]), ...]), ...])` |
| Make a column's cells clickable. | `header(..., mode='link'` |
| Render markdown in a column's cells. | `header(..., mode='md')` |
 
## Styling

| Operation | Style |
|--------|------|
| Left-align text. | `align='left'` |
| Center-align text. | `align='center'` |
| Right-align text. | `align='right'` |
| Justify text. | `align='justify'` |
| Set width. | `width=42` |
| Set height. | `height=42` |
| Set margin (spacing outside border). | `margin=42` |
| Set padding (spacing inside border). | `padding=42` |
| Set text color | `color='#C0FFEE'` |
| Set background color. | `background='#C0FFEE'` |
| Set border color. | `border='#C0FFEE'` |
| Set icon. | `icon=` |
| Set background image. | `text='...', image='sample.jpg'` |
| Set background pattern. | `text, image='pattern.jpg', fit='none'` |
| Scale and clip the image while preserving its aspect ratio. | `fit='cover'` |
| Scale and letterbox the image while preserving its aspect ratio. | `fit='contain'` |
| Stretch the image to fit. | `fit='fill'` |
| Clip the image without resizing. | `fit='none'` |
| Either `contain` or `none`, whichever results in a smaller image. | `fit='scale-down'` |

## Views

| Operation | Code |
|--------|------|
| Overwrite current view | `view(...,)` |
| Overwrite boxes inside box `'foo'`. | `view(..., inside='foo')` |
| Overwrite boxes starting at box `'foo'`. | `view(..., at='foo')` |
| Overwrite boxes before box `'foo'`. | `view(..., before='foo')` |
| Overwrite boxes after box `'foo'`. | `view(..., after='foo')` |
| Append boxes to current view. | `view(..., insert=True)` |
| Append boxes inside box `'foo'`. | `view(..., insert=True, inside='foo')` |
| Insert boxes before box `'foo'`. | `view(..., insert=True, before='foo')` |
| Insert boxes after box `'foo'`. | `view(..., insert=True, after='foo')` |
| Clear current view. | `view(remove=True)` |
| Remove boxes inside box `'foo'`. | `view(remove=True, inside='foo')` |
| Remove boxes starting at box `'foo'`. | `view(remove=True, at='foo')` |
| Remove boxes before box `'foo'`. | `view(remove=True, before='foo')` |
| Remove boxes after box `'foo'`. | `view(remove=True, after='foo')` |
| Show view, but without the "Continue" button. | `view(..., halt=True)` |
| Show view, but don't wait for inputs. | `view(..., read=False)` |
| Show view, but in a popup. | `view(..., popup=True, title='...')` |
| Set view title. | `view.set(title='...')` |
| Set view caption. | `view.set(caption='...')` |
| Set view menu. | `view.set(menu='...')` |
| Set view nav. | `view.set(nav='...')` |
| Set view theme. | `view.set(theme='...')` |
| Jump to another view function. | `view.jump(func)` |
| Jump to another URL. | `view.jump(url)` |
| Jump to another URL in a new window. | `view.jump(url, target='_blank')` |
| Jump to another URL in a new popup window. | `view.jump(url, target='_blank', popup=1)` |

## Layout

| Operation | Code |
|--------|------|
| Stack boxes horizontally. | `box(mode='row', items=[...])` or `row(...)` |
| Stack boxes vertically. | `box(mode='column', items=[...])` or `col(...)` |
| Stack boxes horizontally using tabs. | `box(mode='tabs', items=[...])` |
| Stack boxes vertically using tabs. | `box(mode='tabs', layout='column', items=[...])` |
| Tile boxes from the start. | `tile='start'` |
| Tile boxes around the center. | `tile='center'` |
| Tile boxes towards the end. | `tile='end'` |
| Tile boxes evenly so that the first box is flush with the start, the last is flush with the end. | `tile='between'` |
| Tile boxes evenly so that boxes have a half-size space on either side. | `tile='around'` |
| Tile boxes evenly so that boxes have equal space around them. | `tile='evenly'` |
| Tile boxes using defaults. | `tile='normal.'` |
| Tile boxes from the start (cross-axis). | `cross_tile='start'` |
| Tile boxes around the center (cross-axis). | `cross_tile='center'` |
| Tile boxes towards the end (cross-axis). | `cross_tile='end'` |
| Stretch boxes to fit (cross-axis). | `cross_tile='stretch'` |
| Default alignment (cross-axis). | `cross_tile='normal'` |
| Wrap boxes from the start. | `wrap='start'` |
| Wrap boxes around the center. | `wrap='center'` |
| Wrap boxes towards the end. | `wrap='end'` |
| Wrap boxes evenly so that the first box is flush with the start, the last is flush with the end. | `wrap='between'` |
| Wrap boxes evenly so that boxes have a half-size space on either side. | `wrap='around'` |
| Wrap boxes evenly so that boxes have equal space around them. | `wrap='evenly'` |
| Wrap boxes using defaults. | `wrap='normal.'` |
| Gap (spacing) between boxes. | `gap=42` |
| Amount (parts) of available space to grow to. | `grow=4` |
| Amount (parts) of available space to shrink to. | `shrink=2` |
| Initial size of container to assume for growing or shrinking. | `basis=42` |

