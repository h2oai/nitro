# Styling

Change how boxes look: colors, borders, sizing, margins, and padding.

## Basic

Set `style=` to control how a box looks. Nitro supports [Tailwind](https://tailwindcss.com/) styles.

The following example starts with a plain box and incrementally applies styles to create an alert box.


```py
text = "I'm sorry, Dave. I can't do that."
view(box(text), ['Increase font weight'])
view(box(text, style='font-medium'), ['Make text smaller'])
view(box(text, style='font-medium text-sm'), ['Change text color'])
view(box(text, style='font-medium text-sm text-red-700'), ['Change background color'])
view(box(text, style='font-medium text-sm text-red-700 bg-red-50'), ['Add padding'])
view(box(text, style='font-medium text-sm text-red-700 bg-red-50 p-4'), ['Add border'])
view(box(text, style='font-medium text-sm text-red-700 bg-red-50 p-4 border-l-4'), ['Change border color'])
view(box(text, style='font-medium text-sm text-red-700 bg-red-50 p-4 border-l-4 border-red-700'), ['Restart'])
```


![Screenshot](assets/screenshots/styling_alert.png)


## Card

The following example starts with some nested and incrementally applies styles to create a card.


```py
title = 'Space Travel'
text = lorem(2)
image = box(image='sample.jpg')
view(box(image, box(title), text), ['Resize Card'])
view(box(image, col(box(title), text), style='w-72'), ['Round corners'])
view(box(image, col(box(title), text), style='w-72 rounded-xl'), ['Crop contents'])
view(box(image, col(box(title), text), style='w-72 rounded-xl overflow-hidden'), ['Add shadow'])
view(box(image, col(box(title), text), style='w-72 rounded-xl overflow-hidden shadow-xl'), ['Add padding'])
view(box(image, col(box(title), text, style='p-4'), style='w-72 rounded-xl overflow-hidden shadow-xl'), ['Make title bold'])
view(box(image, col(box(title, style='font-bold'), text, style='p-4'), style='w-72 rounded-xl overflow-hidden shadow-xl'), ['Make title larger'])
view(box(image, col(box(title, style='font-bold text-xl'), text, style='p-4'), style='w-72 rounded-xl overflow-hidden shadow-xl'), ['Make text smaller'])
view(box(image, col(box(title, style='font-bold text-xl'), box(text, style='text-sm'), style='p-4'), style='w-72 rounded-xl overflow-hidden shadow-xl'), ['Restart'])
```


![Screenshot](assets/screenshots/styling_card.png)
