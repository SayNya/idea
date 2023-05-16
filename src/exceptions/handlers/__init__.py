from fastapi import FastAPI

from src.exceptions.handlers.database import include_database_exceptions
from src.exceptions.handlers.http import include_http_exceptions_handlers
from src.exceptions.handlers.validator import include_validators_exceptions_handlers


def include_exceptions_handlers(app: FastAPI):
    include_http_exceptions_handlers(app)
    include_validators_exceptions_handlers(app)
    include_database_exceptions(app)
