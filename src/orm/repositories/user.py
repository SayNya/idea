from datetime import datetime
from typing import Sequence

from sqlalchemy import select, or_, and_
from sqlalchemy.orm import selectinload

from src.orm.async_database import db_session
from src.orm.models import UserModel, TokenModel
from src.orm.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    Model = UserModel

    async def find_by_username(self, username: str) -> Model:
        session = db_session.get()
        query = (
            select(UserModel)
            .options(
                selectinload(UserModel.department),
                selectinload(UserModel.system_roles),
            )
            .filter(or_(UserModel.username == username))
        )
        result = await session.execute(query)
        return result.scalars().first()

    async def get_user_by_token(self, token: str) -> Model:
        session = db_session.get()
        query = (
            select(UserModel)
            .options(
                selectinload(UserModel.token),
                selectinload(UserModel.department),
                selectinload(UserModel.system_roles),
            )
            .filter(
                and_(
                    TokenModel.user_id == UserModel.id,
                    TokenModel.token == token,
                    TokenModel.expires > datetime.now(),
                )
            )
        )
        result = await session.execute(query)
        return result.scalars().first()

    async def get_users_by_ids_and_department_id(
        self, user_ids: list[int], department_id: int
    ) -> Sequence[Model]:
        session = db_session.get()
        query = select(UserModel).filter(
            and_(UserModel.id.in_(user_ids), UserModel.department_id == department_id)
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def get_default_voting_users_by_department_id(
        self, department_id: int
    ) -> Sequence[Model]:
        session = db_session.get()
        query = select(UserModel).filter(
            and_(
                UserModel.department_id == department_id,
                UserModel.is_default_voter,
            )
        )
        result = await session.execute(query)
        return result.scalars().all()
