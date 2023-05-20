from datetime import datetime, timezone

from pydantic import BaseModel, validator


def to_camel_case(snake_case_string: str) -> str:
    string = snake_case_string.replace("_", " ").title().replace(" ", "")
    return string[0].lower() + string[1:]


class BaseRequest(BaseModel):
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class BaseResponse(BaseModel):
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda x: x.replace(tzinfo=timezone.utc).isoformat(
                timespec="seconds"
            ),
        }
