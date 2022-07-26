# Images

Display images, or use them as backgrounds or in patterns.

## Basic

Set `image=` to display an image.


```py
view(box(image='sample.jpg'))
```


Photo by [Ju Guan](https://unsplash.com/@guanju223?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).


![Screenshot](assets/screenshots/image_basic.png)


## Scale and clip images

Set the `object-` style to control how the image should be resized to fit its box.

- `object-cover` (default) scales and *clips* the image while preserving its aspect ratio.
- `object-fill` stretches the image to fit.
- `object-contain` scales and *letterboxes* the image while preserving its aspect ratio.
- `object-none` clips the image without resizing.
- `object-scale-down` behaves like either `contain` or `none`, whichever results in a smaller image.


```py
view(
    row(
        box(image='sample.jpg', style='w-32 h-32 border object-cover'),
        box(image='sample.jpg', style='w-32 h-32 border object-fill'),
        box(image='sample.jpg', style='w-32 h-32 border object-contain'),
        box(image='sample.jpg', style='w-32 h-32 border object-none'),
        box(image='sample.jpg', style='w-32 h-32 border object-scale-down'),
    )
)
```


Photo by [Ju Guan](https://unsplash.com/@guanju223?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).


![Screenshot](assets/screenshots/image_fit.png)


## Use as background

If a box contains child items, `image=` is used as a background.


```py
view(
    col(
        box(
            'To the galaxy and beyond',
            style='font-bold text-3xl text-center text-white',
        ),
        image='sample.jpg',
        style='h-64 justify-center bg-cover bg-center'
    )
)
```


Photo by [Ju Guan](https://unsplash.com/@guanju223?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).


![Screenshot](assets/screenshots/image_background.png)


## Use as pattern

`image=` can also be set to a [Data URI](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs)
with a [base64-encoded](https://en.wikipedia.org/wiki/Base64) image.

The example below uses the image as a background pattern.


```py
view(
    col(
        box(
            'To the galaxy and beyond',
            style='font-bold text-3xl text-center text-white',
        ),
        image='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAEUlEQVQIHWNggIBiEGUFxJUABisBJ85jLc8AAAAASUVORK5CYII=',
        style='h-64 justify-center'
    )
)
```


![Screenshot](assets/screenshots/image_background_pattern.png)
