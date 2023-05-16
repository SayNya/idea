import http

from asyncpg import TooManyConnectionsError
from fastapi import FastAPI, Request, responses


def include_database_exceptions(app: FastAPI):
    @app.exception_handler(TooManyConnectionsError)
    async def too_many_connections_error_handler(
        request: Request, exc: TooManyConnectionsError
    ):
        return responses.JSONResponse(
            content={
                "statusCode": http.HTTPStatus.SERVICE_UNAVAILABLE,
                "detail": "service temporarily unavailable, try again later",
            },
            status_code=http.HTTPStatus.SERVICE_UNAVAILABLE,
        )
