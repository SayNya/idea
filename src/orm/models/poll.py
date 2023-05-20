from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.orm.models.base import BaseIDModel


class PollModel(BaseIDModel):
    __tablename__ = "polls"

    idea_id = Column(Integer, ForeignKey("ideas.id"), nullable=False)
    council_id = Column(Integer, ForeignKey("councils.id"), nullable=False)
    poll_status_id = Column(Integer, ForeignKey("poll_statuses.id"), nullable=False)

    idea = relationship("IdeaModel")  # idea_id
    council = relationship("CouncilModel", back_populates="polls")  # council_id
    poll_status = relationship("PollStatusModel")  # poll_status_id

    votes = relationship("VoteModel", back_populates="poll")
