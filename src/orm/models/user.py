from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.orm.models.base import BaseIDModel


class UserModel(BaseIDModel):
    __tablename__ = "users"

    username = Column(String(50))
    password = Column(String())
    is_active = Column(Boolean(), default=True, nullable=False)

    first_name = Column(String(40), nullable=True)
    last_name = Column(String(40), nullable=True)
    middle_name = Column(String(40), nullable=True)

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    department = relationship("DepartmentModel", back_populates="users")

    token = relationship("TokenModel", back_populates="user")

    def __repr__(self):
        return "<UserModel model {}>".format(self.id)


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
