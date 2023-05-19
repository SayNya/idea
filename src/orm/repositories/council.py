from typing import Sequence

from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from src.orm.async_database import db_session
from src.orm.models import CouncilModel, UserModel
from src.orm.repositories.base import BaseRepository
from src.schemas.enum.council_status import CouncilStatusEnum


class CouncilRepository(BaseRepository):
    Model = CouncilModel

    async def find_active_for_admin(self, department_id: int) -> Model:
        session = db_session.get()
        query = (
            select(CouncilModel)
            .options(
                selectinload(CouncilModel.users)
            )
            .filter(
                and_(
                    CouncilModel.department_id == department_id,
                    CouncilModel.council_status.in_(
                        [
                            CouncilStatusEnum.CREATED,
                            CouncilStatusEnum.PRE_VOTING,
                            CouncilStatusEnum.ONLINE_VOTING,
                        ]
                    ),
                ),
            )
            .order_by(CouncilModel.council_start)
        )
        result = await session.execute(query)
        return result.scalars().first()
