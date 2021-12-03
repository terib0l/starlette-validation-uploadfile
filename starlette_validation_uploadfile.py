from typing import List
from enum import Enum

from starlette import status
from starlette.types import ASGIApp
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

_unsupported_media_type = PlainTextResponse("Unsupported Media Type", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
_length_required = PlainTextResponse("Length Required", status.HTTP_411_LENGTH_REQUIRED)
_request_entity_too_large = PlainTextResponse("Request Entity Too Large", status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

class FileTypeName(str, Enum):
    jpeg = "image/jpeg"
    jpg = "image/jpeg"
    png = "image/png"
    gif = "image/gif"
    webp = "image/webp"
    pdf = "application/pdf"
    zip = "application/zip"
    txt = "text/plain"

class ValidateUploadFileMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        app_path: List[str] = None,
        max_size: int = 16777216, # 16MB
        file_type: List[str] = None
        #file_type: List[FileTypeName] = None
    ) -> None:
        super().__init__(app)
        self.app_path = app_path
        self.max_size = max_size
        self.file_type = file_type

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        scope = request.scope

        if scope["method"] not in ("POST", "PUT"):
            response = await call_next(request)
            return response

        # Check app paths
        if scope["path"] in self.app_path:

            # Check content-type
            if self.file_type:
                form = await request.form()
                content_type = form[next(iter(form))].content_type
                if content_type not in self.file_type:
                    return _unsupported_media_type

            headers = request.headers
            if "content-length" not in headers:
                return _length_required
            # Check content-size
            if int(headers["content-length"]) > self.max_size:
                return _request_entity_too_large

        response = await call_next(request)
        return response
