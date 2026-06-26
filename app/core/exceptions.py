from fastapi import Request
from fastapi.responses import JSONResponse


async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    _ = exc
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
