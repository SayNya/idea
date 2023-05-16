from sqlalchemy import Column, String

from src.orm.models.base import BaseIDModel


class SystemRoleModel(BaseIDModel):
    __tablename__ = "system_roles"

    code = Column(String(255))
    name = Column(String(255))
