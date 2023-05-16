import http

from aiohttp import ClientResponseError
from fastapi import FastAPI, HTTPException, Request, responses

black_list = {"ApplicationException": "something wrong"}


def include_http_exceptions_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        detail = black_list.get(exc.__class__.__name__) or exc.detail

        return responses.JSONResponse(
            content={"statusCode": exc.status_code, "detail": detail},
            status_code=exc.status_code,
        )

    @app.exception_handler(ClientResponseError)
    async def client_response_error_handler(request: Request, exc: ClientResponseError):
        return responses.JSONResponse(
            content={"statusCode": exc.status, "detail": exc.message},
            status_code=exc.status,
        )

    @app.exception_handler(Exception)
    async def other_exceptions_handler(request: Request, exc: ClientResponseError):
        return responses.JSONResponse(
            content={
                "statusCode": http.HTTPStatus.INTERNAL_SERVER_ERROR,
                "detail": "Internal server error",
            },
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        )
