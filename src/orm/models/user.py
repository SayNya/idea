from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import BYTEA
from src.orm.models.base import BaseIDModel


class UserModel(BaseIDModel):
    __tablename__ = "users"

    username = Column(String(50))
    password = Column(BYTEA)
    salt = Column(String)
    is_active = Column(Boolean(), default=True, nullable=False)
    is_default_voter = Column(Boolean, default=False, nullable=True)

    first_name = Column(String(40), nullable=True)
    last_name = Column(String(40), nullable=True)
    middle_name = Column(String(40), nullable=True)

    last_action_at = Column(DateTime)

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    department = relationship("DepartmentModel", back_populates="users")

    token = relationship("TokenModel", back_populates="user")

    ideas = relationship("IdeaModel", secondary="user_idea")
    idea_roles = relationship("IdeaRoleModel", secondary="user_idea")

    system_roles = relationship("SystemRoleModel", secondary="user_system_role")

    def __repr__(self):
        return "<UserModel model {}>".format(self.id)
