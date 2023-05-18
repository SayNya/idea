import datetime

from pydantic import UUID4, Field, validator

from src.schemas.base import BaseResponse
from src.schemas.responses.base import (
    BaseDepartmentResponse,
    BaseSystemRoleResponse,
    BaseUserResponse,
)


class UserAuthResponse(BaseUserResponse):
    department: BaseDepartmentResponse | None
    system_roles: list[BaseSystemRoleResponse] | None


class TokenResponse(BaseResponse):
    token: UUID4
    expires: datetime.datetime
    token_type: str | None = "bearer"

    @validator("token")
    def hexlify_token(cls, value):
        """Конвертирует UUID в hex строку"""
        return value.hex


class TokenUserResponse(UserAuthResponse):
    """Формирует тело ответа с деталями пользователя и токеном"""

    token: TokenResponse = {}
