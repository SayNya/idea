from enum import Enum


class CouncilStatusEnum(str, Enum):
    CREATED = "created"
    PRE_VOTING = "pre_voting"
    ONLINE_VOTING = "online_voting"
    ENDED = "ended"
    COMPLETED = "completed"
