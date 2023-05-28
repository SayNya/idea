from datetime import datetime

from pydantic import Field

from src.schemas.base import BaseResponse
from src.schemas.responses.base import (
    BaseDepartmentResponse,
    BaseIdeaHistoryResponse,
    BaseIdeaCategoryResponse,
    BaseIdeaRoleResponse,
    BaseUserResponse, BaseIdeaResponse,
)




class EmployeeMyIdeasResponse(BaseResponse):
    data: list[BaseIdeaResponse] | None = Field(default_factory=list)
