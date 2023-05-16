import datetime

from pydantic import UUID4, Field, validator, BaseModel

from src.schemas.base import BaseResponse


class UserBaseResponse(BaseResponse):
    """Формирует тело ответа с деталями пользователя"""

    id: int
    username: str


class TokenBaseResponse(BaseResponse):
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime.datetime
    token_type: str | None = "bearer"

    @validator("token")
    def hexlify_token(cls, value):
        """Конвертирует UUID в hex строку"""
        return value.hex


class UserResponse(UserBaseResponse):
    """Формирует тело ответа с деталями пользователя и токеном"""

    token: TokenBaseResponse = {}
