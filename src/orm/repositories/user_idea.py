from src.orm.models import UserIdeaModel
from src.orm.repositories.base import BaseRepository


class UserIdeaRepository(BaseRepository):
    Model = UserIdeaModel
