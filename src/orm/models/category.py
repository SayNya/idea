from sqlalchemy import Boolean, Column, String

from src.orm.models.base import BaseIDModel


class CategoryModel(BaseIDModel):
    __tablename__ = "categories"

    name = Column(String(255))
    is_active = Column(Boolean, default=True)
