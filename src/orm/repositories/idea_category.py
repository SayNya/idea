from src.orm.models import IdeaCategoryModel
from src.orm.repositories.base import BaseRepository


class IdeaCategoryRepository(BaseRepository):
    Model = IdeaCategoryModel
