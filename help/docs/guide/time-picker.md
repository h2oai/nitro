# Time Picker

Use a time picker to pick a time using a 12- or 24-hour clock.

## Basic

Set `mode='time'` to show a time picker.


```py
time = view(box('Set alarm for:', mode='time', value='3:04PM'))
view(f'Alarm set for {time}.')
```


![Screenshot](assets/screenshots/time_basic.png)


## Enable seconds

Include seconds in the `value` to show a seconds component.


```py
time = view(box('Set alarm for:', mode='time', value='3:04:05PM'))
view(f'Alarm set for {time}.')
```


![Screenshot](assets/screenshots/time_seconds.png)


## Show hours only

Exclude minutes and seconds from the `value` to show only the hour component.


```py
time = view(box('Set alarm for:', mode='time', value='3PM'))
view(f'Alarm set for {time}.')
```


![Screenshot](assets/screenshots/time_hour.png)


## Show 24-hour clock

Exclude `AM` or `PM` from the `value` to accept input in military time.


```py
time = view(box('Set alarm for:', mode='time', value='15:04'))
view(f'Alarm set for {time}.')
```


![Screenshot](assets/screenshots/time_24.png)


## Show 24-hour clock, with seconds

Include seconds in the `value` to show a seconds component.


```py
time = view(box('Set alarm for:', mode='time', value='15:04:05'))
view(f'Alarm set for {time}.')
```


![Screenshot](assets/screenshots/time_24_seconds.png)


## Show 24-hour clock, with hour only

Exclude minutes and seconds from the `value` to show only the hour component.


```py
time = view(box('Set alarm for:', mode='time', value='15'))
view(f'Alarm set for {time}.')
```


![Screenshot](assets/screenshots/time_24_hour.png)


## Handle changes immediately

Add `live` to `mode` to handle changes immediately.


```py
time = '3:04PM'
while True:
    time = view(
        box('Set alarm for:', mode='live time', value=time),
        f'Alarm will be set for {time}.',
    )
```


![Screenshot](assets/screenshots/time_live.png)
