from enum import Enum


class IdeaStatusCodeEnum(str, Enum):
    SUBMITTED = "submitted"

    DECLINED = "declined"
    ACCEPTED = "accepted"

    CANCELED = "canceled"
    REALISATION = "realisation"

    COMPLETED = "completed"
