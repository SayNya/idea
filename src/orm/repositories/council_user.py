from src.orm.models import CouncilUserModel
from src.orm.repositories.base import BaseRepository


class CouncilUserRepository(BaseRepository):
    Model = CouncilUserModel
