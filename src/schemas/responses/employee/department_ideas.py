from datetime import datetime

from pydantic import Field

from src.schemas.base import BaseResponse
from src.schemas.responses.base import BaseIdeaResponse


class EmployeeDepartmentIdeasResponse(BaseResponse):
    ideas: list[BaseIdeaResponse] | None = Field(default_factory=list)
