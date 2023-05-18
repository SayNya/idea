from sqlalchemy import select, and_, delete

from src.orm.async_database import db_session
from src.orm.models import UserIdeaModel
from src.orm.repositories.base import BaseRepository


class UserIdeaRepository(BaseRepository):
    Model = UserIdeaModel

    async def find_users_for_idea(
        self, idea_id: int, role_id: int | None = None
    ) -> list[UserIdeaModel]:
        session = db_session.get()
        query = select(UserIdeaModel).filter(
            and_(
                UserIdeaModel.idea_id == idea_id,
            )
        )
        if role_id:
            query = query.filter(
                and_(
                    UserIdeaModel.idea_role_id == role_id,
                )
            )
        result = await session.execute(query)
        return result.scalars().all()

    async def bulk_delete_for_idea_by_role_and_user_ids(
        self, idea_id: int, role_id: int, user_ids: list[int]
    ) -> None:
        session = db_session.get()
        query = delete(UserIdeaModel).filter(
            and_(
                UserIdeaModel.idea_id == idea_id,
                UserIdeaModel.idea_role_id == role_id,
                UserIdeaModel.user_id.in_(user_ids),
            )
        )
        await session.execute(query)
        await session.flush()
