from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from src.orm.models.base import BaseIDModel


class IdeaStatusModel(BaseIDModel):
    __tablename__ = "idea_statuses"

    name = Column(String)
    code = Column(String)

    histories = relationship("IdeaHistoryModel", back_populates="idea_status")
