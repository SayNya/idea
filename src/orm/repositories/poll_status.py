from sqlalchemy import select

from src.orm.async_database import db_session
from src.orm.models import PollStatusModel
from src.orm.repositories.base import BaseRepository
from src.schemas.enum.poll_status import PollStatusCodeEnum


class PollStatusRepository(BaseRepository):
    Model = PollStatusModel

    async def find_by_code(self, code: PollStatusCodeEnum) -> PollStatusModel:
        session = db_session.get()
        query = select(PollStatusModel).filter_by(code=code)
        result = await session.execute(query)
        return result.scalars().first()
