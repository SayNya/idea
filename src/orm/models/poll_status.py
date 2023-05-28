from sqlalchemy import Column, String

from src.orm.models.base import BaseIDModel


class PollStatusModel(BaseIDModel):
    __tablename__ = "poll_statuses"

    name = Column(String)
    code = Column(String)
