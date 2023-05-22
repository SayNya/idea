from src.schemas.responses.base import (
    BaseCouncilResponse,
    BaseUserResponse,
    BasePollResponse,
)


class CouncilDetailsResponse(BaseCouncilResponse):
    polls: list[BasePollResponse]
