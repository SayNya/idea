from src.orm.models import CategoryModel
from src.orm.repositories.base import BaseRepository


class CategoryRepository(BaseRepository):
    Model = CategoryModel
