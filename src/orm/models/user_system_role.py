from sqlalchemy import Column, ForeignKey, Integer

from src.orm.models.base import Base


class UserSystemRoleModel(Base):
    __tablename__ = "user_system_role"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    system_role_id = Column(Integer, ForeignKey("system_roles.id"), primary_key=True)
