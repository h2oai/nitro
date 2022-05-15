# File Upload



## Basic

Set `mode='file'` to show a file upload box.

For file uploads to work correctly, you must define a file upload handler in your
Django, Flask, Starlette, or Tornado application.

The file upload box sends a `multipart/form-data` HTTP `POST` request to the upload
path  (`/upload` by default). The uploaded files are each named `file`. The handler
is expected to process the files and return a JSON response containing a string
array named `files`. This array is returned as-is by `view()` to your Nitro
application code.


```py
filename = view(box('Upload a document', mode='file'))
view(f'You uploaded {filename}.')
```


![Screenshot](assets/screenshots/file_upload_basic.png)


## Allow multiple files

Set `multiple=True` to allow uploading multiple files.


```py
filenames = view(box('Upload some documents', mode='file', multiple=True))
view(f'You uploaded {filenames}.')
```


![Screenshot](assets/screenshots/file_upload_multiple.png)


## Set upload path

Set `path=` to set the path to upload files to.

This is useful if your app's file upload handler path is different from `/upload` (the default),


```py
filename = view(box('Upload a document', mode='file', path='/upload'))
view(f'You uploaded {filename}.')
```


![Screenshot](assets/screenshots/file_upload_path.png)
