from src.orm.models import IdeaHistoryModel
from src.orm.repositories.base import BaseRepository


class IdeaHistoryRepository(BaseRepository):
    Model = IdeaHistoryModel
