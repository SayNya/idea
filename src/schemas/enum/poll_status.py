from enum import Enum


class PollStatusesEnum(str, Enum):
    OPENED = "opened"
    BLOCKED = "blocked"
    ENDED = "ended"
    CLOSED = "closed"
    CANCELED = "canceled"
