import datetime

from pydantic import BaseModel


def to_camel_case(snake_case_string: str) -> str:
    string = snake_case_string.replace("_", " ").title().replace(" ", "")
    return string[0].lower() + string[1:]


class BaseRequest(BaseModel):
    class Config:
        alias_generator = to_camel_case


class BaseResponse(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = to_camel_case
        json_encoders = {
            datetime.datetime: lambda x: x.replace(
                tzinfo=datetime.timezone.utc
            ).isoformat(timespec="seconds"),
        }
