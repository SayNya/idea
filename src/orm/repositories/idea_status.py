from sqlalchemy import select

from src.orm.async_database import db_session
from src.orm.models import IdeaStatusModel
from src.orm.repositories.base import BaseRepository
from src.schemas.enum import IdeaStatusCodeEnum


class IdeaStatusRepository(BaseRepository):
    Model = IdeaStatusModel

    async def find_by_code(self, code: IdeaStatusCodeEnum) -> IdeaStatusModel:
        session = db_session.get()
        query = select(IdeaStatusModel).filter_by(code=code)
        result = await session.execute(query)
        return result.scalars().first()
