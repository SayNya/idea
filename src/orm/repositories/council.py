from datetime import datetime
from typing import Sequence

from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload

from src.orm.async_database import db_session
from src.orm.models import CouncilModel, UserModel, CouncilStatusModel
from src.orm.repositories.base import BaseRepository
from src.schemas.enum.council_status import CouncilStatusCodeEnum


class CouncilRepository(BaseRepository):
    Model = CouncilModel

    async def find_active_for_admin(self, department_id: int) -> Model:
        session = db_session.get()
        query = (
            select(CouncilModel)
            .options(selectinload(CouncilModel.users))
            .filter(
                and_(
                    CouncilModel.department_id == department_id,
                    CouncilModel.council_status_id == CouncilStatusModel.id,
                    CouncilStatusModel.code.in_(
                        [
                            CouncilStatusCodeEnum.CREATED,
                            CouncilStatusCodeEnum.ONLINE_VOTING,
                        ]
                    ),
                ),
            )
            .order_by(CouncilModel.council_start)
        )
        result = await session.execute(query)
        return result.scalars().first()

    async def find_for_scheduler(self) -> Sequence[CouncilModel]:
        session = db_session.get()
        query = select(CouncilModel).filter(
            and_(
                func.DATE(CouncilModel.planned_council_start)
                == datetime.utcnow().date(),
                CouncilModel.council_status_id == CouncilStatusModel.id,
                CouncilStatusModel.code == CouncilStatusCodeEnum.CREATED,
            ),
        )

        result = await session.execute(query)
        return result.scalars().all()

    async def find_with_department(self, council_id: int) -> CouncilModel:
        session = db_session.get()
        query = (
            select(CouncilModel)
            .options(
                selectinload(CouncilModel.department),
                selectinload(CouncilModel.council_status),
            )
            .filter(and_(CouncilModel.id == council_id))
        )
        result = await session.execute(query)
        return result.scalars().first()
