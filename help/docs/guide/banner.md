---
template: overrides/main.html
---
# Banner

Use banners to show errors, warnings, or important information related to an operation.

## Basic

Set `mode=` to `'info'`, `'success'`, `'warning'`, `'critical'`, `'blocked'` or `'error'`  to show a banner.


```py
view(
    box('This server is powered by a lemon and two electrodes.', mode='info'),
    box("The optimizer has been optimized!", mode='success'),
    box('It is pitch black. You are likely to be eaten by a grue.', mode='warning'),
    box('Thermal levels critical. Please wait while we consult the manual.', mode='critical'),
    box('Operation blocked. We are testing your patience.', mode='blocked'),
    box('Operation failed. Something is burning.', mode='error'),
)
```


![Screenshot](assets/screenshots/banner_basic.png)
