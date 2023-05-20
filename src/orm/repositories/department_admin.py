from typing import Sequence, Iterable

from sqlalchemy import select, and_, delete
from sqlalchemy.orm import selectinload

from src.orm.async_database import db_session
from src.orm.models import DepartmentAdminModel, DepartmentModel
from src.orm.repositories.base import BaseRepository


class DepartmentAdminRepository(BaseRepository):
    Model = DepartmentAdminModel

    async def get_department_of_admin(self, user_id: int) -> DepartmentAdminModel:
        session = db_session.get()
        query = (
            select(DepartmentAdminModel)
            .options(selectinload(DepartmentAdminModel.department))
            .filter(
                and_(
                    DepartmentAdminModel.admin_id == user_id,
                    DepartmentAdminModel.department_id == DepartmentModel.id,
                )
            )
        )
        result = await session.execute(query)
        return result.scalars().first()

    async def get_admins_by_department_status(
        self, status: bool
    ) -> Sequence[DepartmentAdminModel]:
        session = db_session.get()
        query = select(DepartmentAdminModel).filter(
            and_(
                DepartmentAdminModel.department_id == DepartmentModel.id,
                DepartmentModel.is_active.is_(status),
            )
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def bulk_delete_admins(
        self, department_ids: Iterable[int], admin_ids: set
    ) -> None:
        session = db_session.get()
        query = delete(DepartmentAdminModel).filter(
            and_(
                DepartmentAdminModel.department_id.in_(department_ids),
                DepartmentAdminModel.admin_id.in_(admin_ids),
            )
        )
        await session.execute(query)
        await session.flush()
