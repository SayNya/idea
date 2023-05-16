from src.orm.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    Model = UserModel

    async def find_by_username(self):
        pass
