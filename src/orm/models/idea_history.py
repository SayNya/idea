from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import relationship

from src.orm.models.base import Base


class IdeaHistoryModel(Base):
    __tablename__ = "idea_history"

    idea_id = Column(Integer, ForeignKey("ideas.id"), primary_key=True)
    idea_status_id = Column(Integer, ForeignKey("idea_statuses.id"), primary_key=True)
    is_current_status = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    idea = relationship("IdeaModel", back_populates="histories")
    status = relationship("StatusModel", back_populates="histories")
