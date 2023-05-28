from sqlalchemy import Column, String

from src.orm.models.base import BaseIDModel


class IdeaRoleModel(BaseIDModel):
    __tablename__ = "idea_roles"

    name = Column(String)
    code = Column(String)
