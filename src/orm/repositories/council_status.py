from typing import Sequence

from sqlalchemy import select, and_

from src.orm.async_database import db_session
from src.orm.models import CouncilStatusModel
from src.orm.repositories.base import BaseRepository
from src.schemas.enum.council_status import CouncilStatusCodeEnum


class CouncilStatusRepository(BaseRepository):
    Model = CouncilStatusModel

    async def find_by_code(self, code: CouncilStatusCodeEnum) -> CouncilStatusModel:
        session = db_session.get()
        query = select(CouncilStatusModel).filter(and_(CouncilStatusModel.code == code))
        result = await session.execute(query)
        return result.scalars().first()
