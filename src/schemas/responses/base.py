from datetime import datetime

from src.schemas.base import BaseResponse


class BaseIdeaCategoryResponse(BaseResponse):
    id: int
    name: str
    is_active: bool


class BaseSystemRoleResponse(BaseResponse):
    id: int
    name: str
    code: str


class BaseDepartmentResponse(BaseResponse):
    id: int
    name: str


class BaseStatusResponse(BaseResponse):
    id: int
    code: str
    title: str


class BaseIdeaHistoryResponse(BaseResponse):
    created_at: datetime
    status: BaseStatusResponse
    is_current_status: bool


class BaseIdeaRoleResponse(BaseResponse):
    id: int
    title: str
    code: str


class BaseUserResponse(BaseResponse):
    id: int
    username: str
    last_name: str | None
    first_name: str | None
    middle_name: str | None
