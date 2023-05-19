from typing import Sequence

from sqlalchemy import select

from src.orm.async_database import db_session
from src.orm.models import CategoryModel
from src.orm.repositories.base import BaseRepository


class CategoryRepository(BaseRepository):
    Model = CategoryModel

    async def find_active_by_ids(self, ids=list[int]) -> Sequence[CategoryModel]:
        session = db_session.get()
        query = select(CategoryModel).filter(
            CategoryModel.id.in_(ids), CategoryModel.is_active
        )
        result = await session.execute(query)
        return result.scalars().all()
