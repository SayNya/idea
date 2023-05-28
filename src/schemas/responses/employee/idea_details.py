from datetime import datetime

from pydantic import Field

from src.schemas.base import BaseResponse
from src.schemas.responses.base import BaseUserResponse, BaseIdeaRoleResponse, BaseDepartmentResponse, \
    BaseIdeaHistoryResponse, BaseIdeaCategoryResponse


class EmployeeMyIdeasUserResponse(BaseUserResponse):
    idea_roles: list[BaseIdeaRoleResponse] = Field(default_factory=list)


class EmployeeIdeaDetailsResponse(BaseResponse):
    id: int
    title: str
    problem_description: str
    solution_description: str
    created_at: datetime
    department: BaseDepartmentResponse | None
    histories: list[BaseIdeaHistoryResponse] | None = Field(default_factory=list)
    users: list[EmployeeMyIdeasUserResponse] | None = Field(default_factory=list)
    categories: list[BaseIdeaCategoryResponse] | None = Field(default_factory=list)
