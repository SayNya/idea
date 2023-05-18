import datetime

from pydantic import BaseModel


def to_camel_case(snake_case_string: str) -> str:
    string = snake_case_string.replace("_", " ").title().replace(" ", "")
    return string[0].lower() + string[1:]


class BaseRequest(BaseModel):
    class Config:
        pass


class BaseResponse(BaseModel):
    class Config:
        orm_mode = True
        json_encoders = {
            datetime.datetime: lambda x: x.replace(
                tzinfo=datetime.timezone.utc
            ).isoformat(timespec="seconds"),
        }
