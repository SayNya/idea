from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from src.orm.models.base import Base


class VoteModel(Base):
    __tablename__ = "votes"

    poll_id = Column(Integer, ForeignKey("polls.id"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    choice = Column(Boolean, nullable=True)

    poll = relationship("PollModel", back_populates="votes")  # poll_id
    user = relationship("UserModel")  # user
