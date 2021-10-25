# starlette-validation-uploadfile

***--- Now, in progress. ---***

[![PyPI](https://img.shields.io/pypi/v/starlette-validation-uploadfile?color=orange)](https://pypi.org/project/starlette-validation-uploadfile/)
[![License](https://img.shields.io/github/license/terib0l/starlette-validation-uploadfile)](https://github.com/terib0l/starlette-validation-uploadfile/blob/main/LICENSE)

Middleware for validation upload-file in FastAPI and Starlette.

## Installation

```bash
pip install starlette-validation-uploadfile
```

## What this package can do:

- Put a limit on the size of the uploaded file
- Restrict the types of files that can be uploaded

## Usage example with FastAPI

The following is almost identical to `test.py`.  
Note: requirements.txt is for test.

```python
from fastapi import FastAPI, Request, UploadFile, File 

from starlette_validation_uploadfile import ValidateUploadFileMiddleware

app = FastAPI()

app.add_middleware(
        ValidateUploadFileMiddleware,
        app_path="/upload/",
        max_size=120000,
        file_type=["image/png", "image/jpeg"]
)

@app.post("/upload/")
def upload_file(request: Request, file: UploadFile = File(...)):
    form = request.form()
    content_type = form[next(iter(form))].content_type

    size = request.headers["content-length"]

    return {
        "filename": file.filename,
        "content_type": content_type,
        "file_size": size
    }
```
