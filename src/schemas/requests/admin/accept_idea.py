from pydantic.types import PositiveInt

from src.schemas.base import BaseRequest


class AcceptIdeaRequest(BaseRequest):
    idea_id: PositiveInt
    is_accepted: bool
