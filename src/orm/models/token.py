from sqlalchemy import Column, DateTime, ForeignKey, Integer, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.orm.models.base import BaseIDModel


class TokenModel(BaseIDModel):
    __tablename__ = "tokens"

    token = Column(
        UUID(as_uuid=False),
        server_default=text("uuid_generate_v4()"),
        unique=True,
        nullable=False,
        index=True,
    )
    expires = Column(DateTime())
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("UserModel", back_populates="token")
