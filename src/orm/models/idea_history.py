from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.orm.models.base import Base


class IdeaHistoryModel(Base):
    __tablename__ = "idea_history"

    idea_id = Column(Integer, ForeignKey("ideas.id"), primary_key=True)
    status_id = Column(Integer, ForeignKey("statuses.id"), primary_key=True)
    is_current_status = Column(Boolean, default=True)

    idea = relationship("IdeaModel", back_populates="histories")
    status = relationship("StatusModel", back_populates="histories")
