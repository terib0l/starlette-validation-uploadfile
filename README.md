# starlette-validation-uploadfile

***--- Now, in progress. ---***

![PyPI](https://img.shields.io/pypi/v/starlette-validation-uploadfile?color=orange)
![License](https://img.shields.io/github/license/terib0l/starlette-validation-uploadfile)

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
        app_path=[
            "/upload/first",
            "/upload/second",
        ],
        max_size=16777216,
        file_type=["image/png", "image/jpeg"]
)

@app.post("/upload/first")
async def upload_file(request: Request, file: UploadFile = File(...)):
    form = await request.form()
    content_type = form[next(iter(form))].content_type

    size = request.headers["content-length"]

    return {
        "filename": file.filename,
        "content_type": content_type,
        "file_size": size,
    }

@app.post("/upload/second")
async def upload_file_second(request: Request, file: UploadFile = File(...)):
    form = await request.form()
    content_type = form[next(iter(form))].content_type

    size = request.headers["content-length"]

    return {
        "filename": file.filename,
        "content_type": content_type,
        "file_size": size,
    }
```
