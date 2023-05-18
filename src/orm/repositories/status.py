from sqlalchemy import select

from src.orm.async_database import db_session
from src.orm.models import StatusModel
from src.orm.repositories.base import BaseRepository


class StatusRepository(BaseRepository):
    Model = StatusModel

    async def find_by_code(self, code: str) -> StatusModel:
        query = select(StatusModel).filter_by(code=code)
        result = await db_session.get().execute(query)
        return result.scalars().first()
