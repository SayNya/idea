from typing import Sequence

from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload, with_loader_criteria

from src.orm.async_database import db_session
from src.orm.models import (
    PollModel,
    IdeaModel,
    IdeaHistoryModel,
    PollStatusModel,
    VoteModel,
)
from src.orm.repositories.base import BaseRepository
from src.schemas.enum import PollStatusCodeEnum


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

    async def find_with_status(self, poll_id: int) -> PollModel:
        session = db_session.get()
        query = (
            select(PollModel)
            .options(selectinload(PollModel.poll_status))
            .filter(and_(PollModel.id == poll_id))
        )
        result = await session.execute(query)
        return result.scalars().first()

    async def find_by_council_id_and_statuses(
        self, council_id: int, statuses: list[PollStatusCodeEnum]
    ) -> Sequence[PollModel]:
        session = db_session.get()
        query = (
            select(PollModel)
            .options(
                selectinload(PollModel.votes),
                with_loader_criteria(VoteModel, VoteModel.choice.is_not(None)),
            )
            .filter(
                and_(
                    PollModel.council_id == council_id,
                    PollModel.poll_status_id == PollStatusModel.id,
                    PollStatusModel.code.in_(statuses),
                )
            )
            .order_by(PollModel.id)
        )
        result = await session.execute(query)
        return result.scalars().all()
