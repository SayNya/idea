from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from src.orm.models import UserModel
from src.orm.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    Model = UserModel

    async def find_by_username(self, username: str):
        query = (
            select(UserModel)
            .options(
                selectinload(UserModel.department),
            )
            .filter(or_(UserModel.username == username))
        )
        result = await self.session.execute(query)
        return result.scalars().first()
