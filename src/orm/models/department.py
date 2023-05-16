from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.orm.models.base import BaseIDModel


class DepartmentModel(BaseIDModel):
    __tablename__ = "departments"

    name = Column(String(255))
    short_name = Column(String(255))

    users = relationship("UserModel", back_populates="department")
    ideas = relationship("IdeaModel", back_populates="department")
