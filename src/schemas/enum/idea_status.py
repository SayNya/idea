from enum import Enum


class IdeaStatusCodeEnum(str, Enum):
    PROPOSED = "proposed"

    DECLINED = "declined"
    ACCEPTED = "accepted"

    REALISATION = "realisation"
