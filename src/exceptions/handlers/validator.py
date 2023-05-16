from http import HTTPStatus

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.responses import JSONResponse


def include_validators_exceptions_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request, exc: RequestValidationError
    ):
        return JSONResponse(
            content=jsonable_encoder({"detail": exc.errors()}),
            status_code=HTTPStatus.BAD_REQUEST,
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request, exc):
        return await request_validation_exception_handler(request, exc)
