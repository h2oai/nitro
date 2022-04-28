# Images



## Basic

Set `image=` to display an image.


```py
view(box(image='sample.jpg'))
```


Photo by [Ju Guan](https://unsplash.com/@guanju223?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).


![Screenshot](assets/screenshots/image_basic.png)


## Set width and height

Images can be resized by setting `width=` or `height=` or both.

- If only `width=` or only `height=` are set, the image is scaled proportionally.
- If both `width=`and`height=`are set, the image is stretched to fit, and might appear distorted.


```py
view(
    box(image='sample.jpg', width=300),
    box(image='sample.jpg', height=200),
    box(image='sample.jpg', width=150, height=300),
)
```


![Screenshot](assets/screenshots/image_resize.png)


## Scale and clip images

Set `fit=` to control how the image should be resized to fit its box.

- `fit='cover'` (default) scales and *clips* the image while preserving its aspect ratio.
- `fit='contain'` scales and *letterboxes* the image while preserving its aspect ratio.
- `fit='fill'` stretches the image to fit.
- `fit='none'` clips the image without resizing.
- `fit='scale-down'` behaves like either `contain` or `none`, whichever results in a smaller image.


```py
style = dict(width=100, height=200)
view(
    row(
        box(image='sample.jpg', fit='cover', **style),
        box(image='sample.jpg', fit='contain', **style),
        box(image='sample.jpg', fit='fill', **style),
        box(image='sample.jpg', fit='none', **style),
        box(image='sample.jpg', fit='scale-down', **style),
    )
)
```


![Screenshot](assets/screenshots/image_fit.png)


## Use as background

If a box contains content, its image is used as a background.

Set `fit=` to control how the background should be resized to fit the box.


```py
style = dict(width=100, height=200, color='white')
view(
    row(
        box('Astro', image='sample.jpg', **style),
        box('Astro', image='sample.jpg', fit='cover', **style),
        box('Astro', image='sample.jpg', fit='contain', **style),
        box('Astro', image='sample.jpg', fit='fill', **style),
        box('Astro', image='sample.jpg', fit='none', **style),
        image='sample.jpg',  # A background for the row as well!
    )
)
```


![Screenshot](assets/screenshots/image_background.png)


## Use as pattern

`image=` can also be set to a [Data URI](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs)
with a [base64-encoded](https://en.wikipedia.org/wiki/Base64) image.

The example below uses `fit='none'` to repeat a small PNG tile horizontally and vertically to form a pattern.


```py
view(box(
    '# Patterns!',
    image='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAEUlEQVQIHWNggIBiEGUFxJUABisBJ85jLc8AAAAASUVORK5CYII=',
    fit='none', height=300
))
```


![Screenshot](assets/screenshots/image_background_pattern.png)
