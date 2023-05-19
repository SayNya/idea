from datetime import datetime

from pydantic.datetime_parse import parse_datetime


class UTCDatetime(datetime):
    @classmethod
    def __get_validators__(cls):
        yield parse_datetime  # default pydantic behavior
        yield cls.ensure_tz_info

    @classmethod
    def ensure_tz_info(cls, v):
        if v.utcoffset():
            return v.replace(tzinfo=None) - v.utcoffset()
        return v.replace(tzinfo=None)

    @staticmethod
    def to_str(dt: datetime) -> str:
        return dt.isoformat()  # replace with w/e format you want
