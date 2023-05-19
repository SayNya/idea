from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.orm.models.base import BaseIDModel


class UserModel(BaseIDModel):
    __tablename__ = "users"

    username = Column(String(50))
    password = Column(String())
    is_active = Column(Boolean(), default=True, nullable=False)

    first_name = Column(String(40), nullable=True)
    last_name = Column(String(40), nullable=True)
    middle_name = Column(String(40), nullable=True)

    is_default_voter = Column(Boolean, default=False, nullable=True)

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    department = relationship("DepartmentModel", back_populates="users")

    token = relationship("TokenModel", back_populates="user")

    ideas = relationship("IdeaModel", secondary="user_idea")
    idea_roles = relationship("IdeaRoleModel", secondary="user_idea")

    system_roles = relationship("SystemRoleModel", secondary="user_system_role")

    def __repr__(self):
        return "<UserModel model {}>".format(self.id)
