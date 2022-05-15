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

If the file upload handler path is different from `/upload`, say `/foo`, set `path=`.
For example, `box('Upload some documents', mode='file', path='/foo')`.


```py
filenames = view(box('Upload some documents', mode='file'))
view(f'You uploaded {filenames}.')
```


![Screenshot](assets/screenshots/file_upload_basic.png)