from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.middleware import RequestIdMiddleware
from app.api.routes.health import router as health_router
from app.api.routes.sort_ticket import router as sort_ticket_router
from app.core.config import get_settings
from app.core.exceptions import unhandled_exception_handler
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    setup_logging(settings)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="QueueStorm Mock API",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.add_middleware(RequestIdMiddleware)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: object, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    app.include_router(health_router)
    app.include_router(sort_ticket_router)
    return app


app = create_app()
