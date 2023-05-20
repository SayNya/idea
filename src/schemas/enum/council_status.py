from enum import Enum


class CouncilStatusCodeEnum(str, Enum):
    CREATED = "created"
    ONLINE_VOTING = "online_voting"
    ENDED = "ended"
