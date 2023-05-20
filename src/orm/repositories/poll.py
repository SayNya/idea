from typing import Sequence

from sqlalchemy import select, and_

from src.orm.async_database import db_session
from src.orm.models import PollModel
from src.orm.repositories.base import BaseRepository


class PollRepository(BaseRepository):
    Model = PollModel

    async def find_by_council_id(self, council_id: int) -> Sequence[PollModel]:
        session = db_session.get()
        query = select(PollModel).filter(and_(PollModel.council_id == council_id))
        result = await session.execute(query)
        return result.scalars().all()

    async def bulk_update(self, poll_ids: list[int], **updates) -> None:
        session = db_session.get()
        query = select(PollModel).filter(PollModel.id.in_(poll_ids))
        result = await session.execute(query)
        polls = result.scalars().all()
        for column, value in updates.items():
            for poll in polls:
                setattr(poll, column, value)
        await session.flush(polls)
