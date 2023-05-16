from sqlalchemy import Column, ForeignKey, Integer

from src.orm.models.base import Base


class IdeaCategoryModel(Base):
    __tablename__ = "category_idea"

    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"), primary_key=True)
