import re
from typing import List
from starlette import status
from starlette.requests import Request
from starlette.types import ASGIApp, Scope, Send, Receive

def validation_error(status_code: int) -> ASGIApp:
    async def send_message(scope: Scope, receive: Receive, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": status_code
            }
        )
        await send({"type": "http.response.body", "body": b"", "more_body": False})

    return send_message

class ValidateUploadFileMiddleware:
    def __init__(self, app: ASGIApp, app_path: str, max_size: int = 120000, file_type: List[str] = None) -> None:
        self.app = app
        self.app_path = re.compile(app_path)
        self.max_size = max_size
        self.file_type = file_type

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        if not self.app_path.fullmatch(scope["path"]) or scope["method"] != "POST":
            await self.app(scope, receive, send)
            return

        request = Request(scope=scope, receive=receive)
        if self.file_type:
            form = await request.form()
            content_type = form[next(iter(form))].content_type
            if content_type not in self.file_type:
                return await validation_error(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)(scope, receive, send)

        if "content-length" not in request.headers:
            return await validation_error(status.HTTP_411_LENGTH_REQUIRED)(scope, receive, send)
        if int(request.headers["content-length"]) > self.max_size:
            return await validation_error(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)(scope, receive, send)

        await self.app(scope, receive, send)
