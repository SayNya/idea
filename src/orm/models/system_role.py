from sqlalchemy import Column, String

from src.orm.models.base import BaseIDModel


class SystemRoleModel(BaseIDModel):
    __tablename__ = "system_roles"

    name = Column(String(255))
    code = Column(String(255))
