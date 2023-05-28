from sqlalchemy import Column, String

from src.orm.models.base import BaseIDModel


class CouncilStatusModel(BaseIDModel):
    __tablename__ = "council_statuses"

    name = Column(String)
    code = Column(String)
