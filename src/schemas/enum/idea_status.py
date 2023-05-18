from enum import Enum


class IdeaStatusCodeEnum(str, Enum):
    PROPOSED = "proposed"

    DECLINED = "declined"
    ACCEPTED = "accepted"

    CANCELED = "canceled"
    REALISATION = "realisation"

    COMPLETED = "completed"
