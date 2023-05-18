from src.orm.models import UserSystemRoleModel
from src.orm.repositories.base import BaseRepository


class UserSystemRoleRepository(BaseRepository):
    Model = UserSystemRoleModel
