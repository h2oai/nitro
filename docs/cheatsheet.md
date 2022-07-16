# Cheatsheet

## Widgets

| Output | Code |
|--------|------|
| Stack boxes horizontally. | `box(mode='row', items=[...])` or `row(...)` |
| Stack boxes vertically. | `box(mode='column', items=[...])` or `col(...)` |
| Stack boxes horizontally using tabs. | `box(mode='tabs', items=[...])` |
| Stack boxes vertically using tabs. | `box(mode='tabs', layout='column', items=[...])` |
| Render markdown. | `box(mode='md')` |
| Show a textbox. | `box(mode='text')` |
| Show a spinbox. | `box(mode='number')` |
| Show a checkbox. | `box(mode='check')` |
| Show a checklist. | `box(mode='check', options=[...])` |
| Show a toggle. | `box(mode='toggle')` |
| Show buttons stacked horizontally. | `box(mode='button', options=[...])` or `box([...])` |
| Show buttons stacked vertically. | `box(mode='button', layout='column', options=[...])` |
| Show buttons with captions (compound buttons). | `box(mode='button', options=[option(..., caption='...'), ...])` |
| Show buttons with menus (split buttons). | `box(mode='button', options=[option(..., options=[...]), ...])` |
| Show radio buttons. | `box(mode='radio', options=[...])` |
| Show a dropdown menu (single-select). | `box(mode='menu', options=[...])` |
| Show a dropdown menu (multi-select). | `box(mode='menu', options=[...], multiple=True)` |
| Show a dropdown menu with arbitrary text input (combo box). | `box(mode='menu', options=[...], editable=True)` |
| Show a dropdown menu grouped options. | `box(mode='menu', options=[option(..., options=[...]), ...])` |
| Show a table | `box(mode='table', headers=[...], options=[option(..., options=[...]), ...])` |
| Make a column's cells clickable. | `box(mode='table', headers=[header(..., mode='link'), ...], options=[option(..., options=[...]), ...])` |
| Render markdown in a column's cells. | `box(mode='table', headers=[header(..., mode='md'), ...], options=[option(..., options=[...]), ...])` |
| Show a table with multi-select rows. | `box(mode='table', headers=[...], options=[option(..., options=[...]), ...], multiple=True)` |
| Show a table with single-select rows. | `box(mode='table', headers=[...], options=[option(..., options=[...]), ...], multiple=False)` |
| Show a table with grouped rows. | `box(mode='table', headers=[...], options=[option(..., options=[option(..., options=[...]), ...]), ...])` |
| Show a slider. | `box(mode='range')` |
| Show a range slider. | `box(mode='range', value=(min, max))` |
| Show a time picker. | `box(mode='time')` |
| Show a date picker. | `box(mode='date')` |
| Show a week picker. | `box(mode='week')` |
| Show a month picker. | `box(mode='month')` |
| Show a calendar. | `box(mode='day')` |
| Show a tag picker. | `box(mode='tag', options=[...])` |
| Show a color picker. | `box(mode='color')` |
| Show a color palette. | `box(mode='color', options=[...])` |
| Show a star-rating. | `box(mode='rating')` |
| Show a file uploader. | `box(mode='file')` |
| Show a indeterminate progress bar. | `box(mode='progress')` |
| Show a progress bar. | `box(mode='progress', value=x)` |
| Show a spinner. | `box(mode='spinner')` |
| Show a separator. | `box(mode='separator')` |
| Show an image. | `box(image='...')` |
| Show and scale an image. | `box(image='...', fit='...')` |
| Show a web view (`iframe`). | `box(mode='web')` |

## Layout

| Operation | Setting |
|--------|------|
| Layout items vertically. | `layout='column'` |
| Layout items horizontally. | `layout='row'` |
| Pack items from the start. | `tile='start'` |
| Pack items around the center. | `tile='center'` |
| Pack items towards the end. | `tile='end'` |
| Distribute items evenly. The first item is flush with the start, the last is flush with the end. | `tile='between'` |
| Distribute items evenly. Items have a half-size space on either side. | `tile='around'` |
| Distribute items evenly. Items have equal space around them. | `tile='evenly'` |
| Default alignment. | `tile='normal.'` |
| Pack items from the start. | `cross_tile='start'` |
| Pack items around the center. | `cross_tile='center'` |
| Pack items towards the end. | `cross_tile='end'` |
| Stretch items to fit. | `cross_tile='stretch'` |
| Default alignment. | `cross_tile='normal'` |
| Pack items from the start. | `wrap='start'` |
| Pack items around the center. | `wrap='center'` |
| Pack items towards the end. | `wrap='end'` |
| Distribute items evenly. The first item is flush with the start, the last is flush with the end. | `wrap='between'` |
| Distribute items evenly. Items have a half-size space on either side. | `wrap='around'` |
| Distribute items evenly. Items have equal space around them. | `wrap='evenly'` |
| Default alignment. | `wrap='normal.'` |
| Gap (spacing) between items. | `gap=N` |
| Amount of of available space to grow to. | `grow=N` |
| Amount of of available space to shrink to. | `shrink=N` |
| Initial size of container to assume for growing or shrinking. | `basis=N` |
 
## Styling

| Operation | Setting |
|--------|------|
| Left-align text. | `align='left'` |
| Center-align text. | `align='center'` |
| Right-align text. | `align='right'` |
| Justify text. | `align='justify'` |
| Set width. | `width=N` |
| Set height. | `height=N` |
| Set margin (spacing outside border). | `margin=N` |
| Set padding (spacing inside border). | `padding=N` |
| Set text color | `color='#C0FFEE'` |
| Set background color. | `background='#C0FFEE'` |
| Set border color. | `border='#C0FFEE'` |
| Set icon. | `icon=` |
| Set image background. | `text='...', image='sample.jpg'` |
| Set background pattern. | `text, image='pattern.jpg', fit='none'` |
| Scale and clip the image while preserving its aspect ratio. | fit='cover' |
| Scale and letterbox the image while preserving its aspect ratio. | fit='contain' |
| Stretch the image to fit. | fit='fill' |
| Clip the image without resizing. | fit='none' |
| Either `contain` or `none`, whichever results in a smaller image. | fit='scale-down' |


