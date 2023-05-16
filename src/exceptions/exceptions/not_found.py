import http

from src.exceptions.exceptions.application import ApplicationException


class NotFoundException(ApplicationException):
    status_code = http.HTTPStatus.NOT_FOUND
    detail = "Not found"
