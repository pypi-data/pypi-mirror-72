from typing import Any

from fastapi.responses import FileResponse  # type:ignore

from pullframe.types import Request as Request

app: Any

async def root(request: Request) -> FileResponse: ...
