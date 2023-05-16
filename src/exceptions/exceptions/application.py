import http
from typing import Any

from fastapi import HTTPException


class ApplicationException(HTTPException):
    status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
    detail = "something is wrong"

    def __init__(self, status_code: int = None, detail: Any = None):
        super(ApplicationException, self).__init__(
            status_code=status_code or self.status_code, detail=detail or self.detail
        )
