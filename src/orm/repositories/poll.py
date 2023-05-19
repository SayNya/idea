from src.orm.models import PollModel
from src.orm.repositories.base import BaseRepository


class PollRepository(BaseRepository):
    Model = PollModel
