from sqlalchemy import select, and_
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

