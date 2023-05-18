from src.orm.models import StatusModel
from src.orm.repositories.base import BaseRepository


class StatusRepository(BaseRepository):
    Model = StatusModel
