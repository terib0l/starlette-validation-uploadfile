from fastapi import FastAPI, Request, UploadFile, File 
from fastapi.responses import RedirectResponse

from starlette_validation_uploadfile import ValidateUploadFileMiddleware
#from tmp.override_ver import ValidateUploadFileMiddleware

app = FastAPI()

app.add_middleware(
        ValidateUploadFileMiddleware,
        app_path="/upload/",
        max_size=120000,
        file_type=["image/jpeg"]
)

@app.get("/", response_class=RedirectResponse)
def index(request: Request):
    return request.url_for("index") + "docs"

@app.post("/upload/")
def upload_file(request: Request, file: UploadFile = File(...)):
    form = request.form()
    content_type = form[next(iter(form))].content_type

    size = request.headers["content-length"]

    return {
        "filename": file.filename,
        "content_type": content_type,
        "file_size": size,
    }
