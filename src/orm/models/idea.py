from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.orm.models.base import BaseIDModel


class IdeaModel(BaseIDModel):
    __tablename__ = "ideas"

    title = Column(String(length=300))
    problem_description = Column(String(length=2000))
    solution_description = Column(String(length=2000))

    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("DepartmentModel", back_populates="ideas")

    histories = relationship(
        "IdeaHistoryModel",
        back_populates="idea",
        order_by="desc(IdeaHistoryModel.created_at)",
    )

    employees = relationship("EmployeesIdeasModel", back_populates="idea")
    categories = relationship("CategoryModel", secondary="idea_category")

    is_in_release = Column(Boolean, default=False)
