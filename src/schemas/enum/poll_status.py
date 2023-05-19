from enum import Enum


class PollStatusCodeEnum(str, Enum):
    OPENED = "opened"
    BLOCKED = "blocked"
    ENDED = "ended"
    CLOSED = "closed"
    CANCELED = "canceled"
