from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.orm.models.base import Base


class DepartmentAdminModel(Base):
    __tablename__ = "department_admin"

    admin_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    department_id = Column(Integer, ForeignKey("departments.id"), primary_key=True)

    department = relationship(
        "DepartmentModel", backref="department_admins"
    )  # department_id
    admin = relationship("UserModel")  # admin_id
