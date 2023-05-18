from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.orm.models.base import BaseIDModel


class CouncilModel(BaseIDModel):
    __tablename__ = "councils"

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    chairman_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    council_status_id = Column(
        Integer, ForeignKey("council_statuses.id"), nullable=False
    )

    council_start = Column(DateTime)
    planned_council_start = Column(DateTime, nullable=False)
    council_end = Column(DateTime)

    department = relationship("DepartmentModel")  # department_id
    chairman = relationship("UserModel")  # chairman_id
    council_status = relationship("CouncilStatusModel")  # council_status_id

    users = relationship(
        "UserModel",
        secondary="council_user",
    )
    polls = relationship("PollModel", order_by="PollModel.id")
