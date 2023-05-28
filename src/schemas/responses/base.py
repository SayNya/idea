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


class BaseIdeaStatusResponse(BaseResponse):
    id: int
    code: str
    title: str


class BaseIdeaHistoryResponse(BaseResponse):
    created_at: datetime
    idea_status: BaseIdeaStatusResponse
    is_current_status: bool


class BaseIdeaRoleResponse(BaseResponse):
    id: int
    title: str
    code: str


class BaseIdeaResponse(BaseResponse):
    id: int
    title: str
    created_at: datetime


class BaseUserResponse(BaseResponse):
    id: int
    username: str
    last_name: str | None
    first_name: str | None
    middle_name: str | None


class BaseCouncilStatusResponse(BaseResponse):
    id: int
    title: str
    code: str


class BaseVoteResponse(BaseResponse):
    user_id: int
    choice: bool | None


class BasePollStatusResponse(BaseResponse):
    id: int
    title: str
    code: str


class BasePollResponse(BaseResponse):
    poll_status: BasePollStatusResponse
    idea: BaseIdeaResponse
    votes: list[BaseVoteResponse] | None


class BaseCouncilResponse(BaseResponse):
    id: int
    council_status: BaseCouncilStatusResponse
    planned_council_start: datetime
    council_start: datetime | None = None
    council_end: datetime | None = None
