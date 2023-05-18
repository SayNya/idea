from datetime import datetime

from sqlalchemy import select, or_, and_
from sqlalchemy.orm import selectinload

from src.orm.async_database import db_session
from src.orm.models import UserModel, TokenModel
from src.orm.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    Model = UserModel

    async def find_by_username(self, username: str) -> Model:
        query = (
            select(UserModel)
            .options(
                selectinload(UserModel.department),
                selectinload(UserModel.system_roles),
            )
            .filter(or_(UserModel.username == username))
        )
        result = await db_session.get().execute(query)
        return result.scalars().first()

    async def get_user_by_token(self, token: str) -> Model:
        query = (
            select(UserModel)
            .options(
                selectinload(UserModel.token),
                selectinload(UserModel.department),
                selectinload(UserModel.system_roles),
            )
            .filter(
                and_(TokenModel.token == token, TokenModel.expires > datetime.now())
            )
        )
        result = await db_session.get().execute(query)
        return result.scalars().first()
