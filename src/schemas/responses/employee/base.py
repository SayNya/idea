from pydantic import Field

from src.schemas.base import BaseResponse


class BaseIdeaCategoriesResponse(BaseResponse):
    id: int
    name: str
    is_active: bool
    color: str | None


class BaseIdeaRoleResponse(BaseResponse):
    id: int
    title: str
    code: str


class BaseUserResponse(BaseResponse):
    id: int
    first_name: str | None
    last_name: str | None
    middle_name: str | None
