from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from src.orm.models.base import BaseIDModel


class StatusModel(BaseIDModel):
    __tablename__ = "statuses"

    title = Column(String)
    code = Column(String)
    description = Column(Text, nullable=True)

    histories = relationship("IdeaHistoryModel", back_populates="status")
