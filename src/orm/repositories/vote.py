from sqlalchemy import update

from src.orm.async_database import db_session
from src.orm.models import VoteModel
from src.orm.repositories.base import BaseRepository


class VoteRepository(BaseRepository):
    Model = VoteModel

    async def update_choice_by_user_and_poll_ids(
        self, employee_id: int, poll_id: int, choice: bool
    ) -> None:
        session = db_session.get()
        query = (
            update(VoteModel)
            .filter_by(user_id=employee_id, poll_id=poll_id)
            .values(choice=choice)
        )
        await session.execute(query)
        await session.commit()
