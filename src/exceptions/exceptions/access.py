import http

from src.exceptions.exceptions.application import ApplicationException


class AccessDeniedException(ApplicationException):
    status_code = http.HTTPStatus.FORBIDDEN
    detail = "access denied"
