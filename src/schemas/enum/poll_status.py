from enum import Enum


class PollStatusCodeEnum(str, Enum):
    BLOCKED = "blocked"
    OPENED = "opened"
    ENDED = "ended"
