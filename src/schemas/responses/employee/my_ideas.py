from datetime import datetime

from pydantic import Field


from src.schemas.base import BaseResponse
from src.schemas.responses.employee.base import (
    BaseIdeaCategoriesResponse,
    BaseIdeaRoleResponse, BaseUserResponse,
)


class EmployeeMyIdeasDepartmentResponse(BaseResponse):
    id: int
    name: str


class EmployeeMyIdeasStatusResponse(BaseResponse):
    code: str
    title: str


class EmployeeMyIdeasHistoryResponse(BaseResponse):
    id: int
    created_at: datetime
    status: EmployeeMyIdeasStatusResponse
    is_current_status: bool


class EmployeeMyIdeasUserResponse(BaseUserResponse):
    idea_roles: list[BaseIdeaRoleResponse] = Field(default_factory=list)


class EmployeeMyIdeasDetailsResponse(BaseResponse):
    id: int
    title: str
    created_at: datetime
    department: EmployeeMyIdeasDepartmentResponse | None
    histories: list[EmployeeMyIdeasHistoryResponse] | None = Field(default_factory=list)
    users: list[EmployeeMyIdeasUserResponse] | None = Field(default_factory=list)
    categories: list[BaseIdeaCategoriesResponse] | None = Field(default_factory=list)


class EmployeeMyIdeasResponse(BaseResponse):
    data: list[EmployeeMyIdeasDetailsResponse] | None = Field(default_factory=list)
