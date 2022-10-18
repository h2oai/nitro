---
template: overrides/main.html
---
# File Upload

Use a file upload component to get one or more files from the user.

## Basic

Set `mode='file'` to show a file upload box.

For file uploads to work correctly, you must define a file upload handler in your
Django, Flask, Starlette, or Tornado application.

The file upload box sends a `multipart/form-data` HTTP `POST` request to the upload
location (`/upload` by default). The uploaded files are each named `file`. The handler
is expected to process the files and return a JSON response containing a string
array named `files`. This array is returned as-is by `view()` to your Nitro
application code.


```py
filename = view(box('Upload a document', mode='file'))
view(f'You uploaded {filename}.')
```


![Screenshot](assets/screenshots/file_upload_basic.png)


## Allow multiple files

Add `multi` to `mode` to allow uploading multiple files.


```py
filenames = view(box('Upload some documents', mode='multi file'))
view(f'You uploaded {filenames}.')
```


![Screenshot](assets/screenshots/file_upload_multiple.png)


## Set upload location

Set `link=` to set the location to upload files to.

This is necessary if your app's file upload handler location is different from `/upload` (the default),


```py
filename = view(box('Upload a document', mode='file', link='/upload'))
view(f'You uploaded {filename}.')
```


![Screenshot](assets/screenshots/file_upload_path.png)


## Disable

Set `disabled=True` to disable.


```py
view(box('Upload a document', mode='file', disabled=True))
```


![Screenshot](assets/screenshots/file_upload_disable.png)
