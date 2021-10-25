import re
from typing import List
from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

class ValidateUploadFileMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, app_path: str, max_size: int = 120000, file_type: List[str] = None) -> None:
        super().__init__(app)
        self.app_path = re.compile(app_path)
        self.max_size = max_size
        self.file_type = file_type

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if self.app_path.match(request.scope["path"]) and request.method == "POST":
            if self.file_type:
                form = await request.form()
                content_type = form[next(iter(form))].content_type
                if content_type not in self.file_type:
                    return Response(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

            if "content-length" not in request.headers:
                return Response(status_code=status.HTTP_411_LENGTH_REQUIRED)
            if int(request.headers["content-length"]) > self.max_size:
                return Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        print("testtest")
        response = await call_next(request)
        return response
