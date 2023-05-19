from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import relationship

from src.orm.models.base import BaseIDModel


class IdeaHistoryModel(BaseIDModel):
    __tablename__ = "idea_history"

    idea_id = Column(Integer, ForeignKey("ideas.id"))
    idea_status_id = Column(Integer, ForeignKey("idea_statuses.id"))
    is_current_status = Column(Boolean, default=True)

    idea = relationship("IdeaModel", back_populates="histories")
    idea_status = relationship("IdeaStatusModel", back_populates="histories")
