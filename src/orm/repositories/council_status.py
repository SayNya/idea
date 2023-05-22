from typing import Sequence

from sqlalchemy import select

from src.orm.async_database import db_session
from src.orm.models import CouncilStatusModel
from src.orm.repositories.base import BaseRepository
from src.schemas.enum.council_status import CouncilStatusCodeEnum


class CouncilStatusRepository(BaseRepository):
    Model = CouncilStatusModel

    async def find_by_codes(
        self, codes: list[CouncilStatusCodeEnum]
    ) -> Sequence[CouncilStatusModel]:
        session = db_session.get()
        query = select(CouncilStatusModel).filter(CouncilStatusModel.code.in_(codes))
        result = await session.execute(query)
        return result.scalars().all()
