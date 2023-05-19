import datetime

from pydantic.class_validators import validator
from pydantic.types import PositiveInt, conlist

from src.orm.types import UTCDatetime
from src.schemas.base import BaseRequest


class ConveneCouncilRequest(BaseRequest):
    voting_users_ids: conlist(item_type=int, unique_items=True, min_items=1)
    planned_council_start: UTCDatetime
    chairman_id: PositiveInt

    @validator("chairman_id")
    def validate_chairman_id(cls, v, values):
        if v not in values.get("voting_users_ids"):
            raise ValueError("chairman also must be in list of voting users")
        return v

    @validator("planned_council_start")
    def validate_council_start(cls, v):
        if v < datetime.datetime.utcnow():
            raise ValueError("start of council can't be in the past")
        return v
