from src.orm.models import TokenModel
from src.orm.repositories.base import BaseRepository


class TokenRepository(BaseRepository):
    Model = TokenModel
