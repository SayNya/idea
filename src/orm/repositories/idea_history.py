from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from src.orm.async_database import db_session
from src.orm.models import IdeaHistoryModel
from src.orm.repositories.base import BaseRepository


class IdeaHistoryRepository(BaseRepository):
    Model = IdeaHistoryModel

    async def find_current_idea_status(self, idea_id: int) -> Model:
        session = db_session.get()
        query = (
            select(IdeaHistoryModel)
            .options(selectinload(IdeaHistoryModel.idea_status))
            .filter(
                and_(
                    IdeaHistoryModel.idea_id == idea_id,
                    IdeaHistoryModel.is_current_status,
                )
            )
        )
        result = await session.execute(query)
        return result.scalars().first()
