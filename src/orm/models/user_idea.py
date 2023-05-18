from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from src.orm.models.base import Base


class UserIdeaModel(Base):
    __tablename__ = "user_idea"

    idea_id = Column(Integer, ForeignKey("ideas.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    idea_role_id = Column(Integer, ForeignKey("idea_roles.id"), primary_key=True)

