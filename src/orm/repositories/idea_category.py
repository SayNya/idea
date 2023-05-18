from typing import Iterable, Sequence

from sqlalchemy import delete, and_, select

from src.orm.async_database import db_session
from src.orm.models import IdeaCategoryModel
from src.orm.repositories.base import BaseRepository


class IdeaCategoryRepository(BaseRepository):
    Model = IdeaCategoryModel

    async def find_by_idea_id(self, idea_id: int) -> Sequence[IdeaCategoryModel]:
        session = db_session.get()
        query = select(IdeaCategoryModel).filter_by(idea_id=idea_id)
        result = await session.execute(query)
        return result.scalars().all()

    async def bulk_delete_categories(
        self, category_ids: Iterable[int], idea_id: int
    ) -> None:
        session = db_session.get()
        query = delete(IdeaCategoryModel).filter(
            and_(
                IdeaCategoryModel.category_id.in_(category_ids),
                IdeaCategoryModel.idea_id == idea_id,
            )
        )
        await session.execute(query)
        await session.flush()
