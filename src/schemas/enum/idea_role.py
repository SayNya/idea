from enum import Enum


class IdeaRoleEnum(str, Enum):
    IDEA_AUTHOR = "idea_author"
    IDEA_COAUTHOR = "idea_coauthor"
    IDEA_RESPONSIBLE = "idea_responsible"
