from fastapi import FastAPI, Request, UploadFile, File 
from fastapi.responses import RedirectResponse

from starlette_validation_uploadfile import ValidateUploadFileMiddleware

app = FastAPI()

app.add_middleware(
        ValidateUploadFileMiddleware,
        app_path=[
            "/upload/first",
        ], 
        max_size=12000,
        file_type=["image/jpeg"]
)

@app.get("/", response_class=RedirectResponse)
def index(request: Request):
    return request.url_for("index") + "docs"

@app.post("/upload/first")
async def upload_file_first(request: Request, file: UploadFile = File(...)):
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
