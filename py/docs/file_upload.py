# Copyright 2022 H2O.ai, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from h2o_nitro import View, box, row, col, option, lorem


# # File Upload

# ## Basic
# Set `mode='file'` to show a file upload box.
#
# For file uploads to work correctly, you must define a file upload handler in your
# Django, Flask, Starlette, or Tornado application.
#
# The file upload box sends a `multipart/form-data` HTTP `POST` request to `/upload`.
# The uploaded files are each named `file`. The handler is expected to process the files
# and return a JSON response containing a string array named `files`. This array
# is returned as-is by `view()` to your Nitro application code.
def file_upload_basic(view: View):
    filenames = view(box('Upload some documents', mode='file'))
    view(f'You uploaded {filenames}.')
