# Time Picker



## Basic

Set `mode='time'` to show a time picker.


```py
time = view(box('Set alarm for:', mode='time', value='3:04PM'))
view(f'Alarm set for {time}.')
```


![Screenshot](assets/screenshots/time_basic.png)


## With seconds

Include seconds in the `value` to show a seconds component.


```py
time = view(box('Set alarm for:', mode='time', value='3:04:05PM'))
view(f'Alarm set for {time}.')
```


![Screenshot](assets/screenshots/time_seconds.png)


## Hour only

Exclude minutes and seconds from the `value` to show only the hour component.


```py
time = view(box('Set alarm for:', mode='time', value='3PM'))
view(f'Alarm set for {time}.')
```


![Screenshot](assets/screenshots/time_hour.png)


## 24-hour clock

Exclude `AM` or `PM` from the `value` to accept input in military time.


```py
time = view(box('Set alarm for:', mode='time', value='15:04'))
view(f'Alarm set for {time}.')
```


![Screenshot](assets/screenshots/time_24.png)


## 24-hour clock, with seconds

Include seconds in the `value` to show a seconds component.


```py
time = view(box('Set alarm for:', mode='time', value='15:04:05'))
view(f'Alarm set for {time}.')
```


![Screenshot](assets/screenshots/time_24_seconds.png)


## 24-hour clock, hour only

Exclude minutes and seconds from the `value` to show only the hour component.


```py
time = view(box('Set alarm for:', mode='time', value='15'))
view(f'Alarm set for {time}.')
```


![Screenshot](assets/screenshots/time_24_hour.png)
