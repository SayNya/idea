from typing import Sequence

from sqlalchemy import select, and_, desc
from sqlalchemy.orm import selectinload, with_loader_criteria

from src.orm.async_database import db_session
from src.orm.models import (
    IdeaModel,
    UserIdeaModel,
    UserModel,
    IdeaHistoryModel,
)
from src.orm.repositories.base import BaseRepository


class IdeaRepository(BaseRepository):
    Model = IdeaModel

    async def find_by_user(
        self, user_id: int, role_ids: list[int]
    ) -> Sequence[IdeaModel]:
        query = (
            select(IdeaModel)
            .options(
                selectinload(IdeaModel.users).options(
                    selectinload(UserModel.idea_roles),
                ),
                with_loader_criteria(
                    UserIdeaModel,
                    and_(
                        UserIdeaModel.user_id == user_id,
                        UserIdeaModel.idea_role_id.in_(role_ids),
                    ),
                ),
            )
            .options(
                selectinload(IdeaModel.histories).selectinload(IdeaHistoryModel.status),
                with_loader_criteria(
                    IdeaHistoryModel, IdeaHistoryModel.is_current_status.is_(True)
                ),
            )
            .options(
                selectinload(IdeaModel.categories),
            )
            .options(
                selectinload(IdeaModel.department),
            )
        )

        query = query.order_by(desc(IdeaModel.created_at)).distinct()

        result = await db_session.get().execute(query)
        return result.scalars().all()
