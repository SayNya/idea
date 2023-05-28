from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from src.orm.models.base import BaseIDModel


class DepartmentModel(BaseIDModel):
    __tablename__ = "departments"

    name = Column(String(255))
    is_active = Column(Boolean, default=True)

    users = relationship("UserModel", back_populates="department")
    ideas = relationship("IdeaModel", back_populates="department")
