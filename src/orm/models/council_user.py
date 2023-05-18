from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.orm.models.base import Base


class CouncilUserModel(Base):
    __tablename__ = "council_user"

    council_id = Column(
        Integer,
        ForeignKey("councils.id"),
        primary_key=True,
        nullable=False,
    )
    user_id = Column(
        Integer, ForeignKey("users.id"), primary_key=True, nullable=False
    )

    council = relationship("CouncilModel")  # council_id
    user = relationship("UserModel")  # user_id
