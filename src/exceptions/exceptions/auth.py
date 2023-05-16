import http

from src.exceptions.exceptions.application import ApplicationException


class UnauthorizedException(ApplicationException):
    status_code = http.HTTPStatus.UNAUTHORIZED
    detail = "can't authorize"
