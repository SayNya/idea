from typing import Sequence

from sqlalchemy import select, and_, desc
from sqlalchemy.orm import selectinload, with_loader_criteria

from src.orm.async_database import db_session
from src.orm.models import (
    IdeaModel,
    UserIdeaModel,
    UserModel,
    IdeaHistoryModel,
    IdeaRoleModel,
)
from src.orm.repositories.base import BaseRepository
from src.schemas.enum import IdeaRoleCodeEnum, IdeaStatusCodeEnum


class IdeaRepository(BaseRepository):
    Model = IdeaModel

    async def find_by_user(
        self, user_id: int, role_ids: list[int]
    ) -> Sequence[IdeaModel]:
        session = db_session.get()
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
                selectinload(IdeaModel.histories).selectinload(
                    IdeaHistoryModel.idea_status
                ),
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

        result = await session.execute(query)
        return result.scalars().all()

    async def find_by_idea_id(
        self, idea_id: int
    ) -> Sequence[IdeaModel]:
        session = db_session.get()
        query = (
            select(IdeaModel)
            .options(
                selectinload(IdeaModel.users).options(
                    selectinload(UserModel.idea_roles),
                ),
            )
            .options(
                selectinload(IdeaModel.histories).selectinload(
                    IdeaHistoryModel.idea_status
                ),
            )
            .options(
                selectinload(IdeaModel.categories),
            )
            .options(
                selectinload(IdeaModel.department),
            )
            .filter(
                and_(
                    IdeaModel.id == idea_id
                )
            )
        )

        result = await session.execute(query)
        return result.scalars().first()

    async def find_for_employee(self, idea_id: int, employee_id: int) -> IdeaModel:
        session = db_session.get()
        query = (
            select(IdeaModel)
            .options(
                selectinload(IdeaModel.histories).options(
                    selectinload(IdeaHistoryModel.idea_status),
                ),
                with_loader_criteria(
                    IdeaHistoryModel, IdeaHistoryModel.is_current_status.is_(True)
                ),
            )
            .filter(
                and_(
                    IdeaModel.id == idea_id,
                    UserIdeaModel.idea_id == IdeaModel.id,
                    UserModel.id == UserIdeaModel.user_id,
                    UserModel.id == employee_id,
                    UserIdeaModel.idea_role_id == IdeaRoleModel.id,
                    IdeaRoleModel.code == IdeaRoleCodeEnum.IDEA_AUTHOR,
                )
            )
        )
        result = await session.execute(query)
        return result.scalars().first()

    async def find_with_history(self, idea_id: int) -> IdeaModel:
        session = db_session.get()
        query = (
            select(IdeaModel)
            .options(
                selectinload(IdeaModel.histories).options(
                    selectinload(IdeaHistoryModel.idea_status),
                ),
                with_loader_criteria(
                    IdeaHistoryModel, IdeaHistoryModel.is_current_status.is_(True)
                ),
            )
            .filter(
                and_(
                    IdeaModel.id == idea_id,
                )
            )
        )
        result = await session.execute(query)
        return result.scalars().first()

    async def find_proposed_ideas_by_status_and_department(
        self, status_id: int, department_id: int
    ) -> Sequence[IdeaModel]:
        session = db_session.get()
        query = select(IdeaModel).filter(
            and_(
                IdeaModel.department_id == department_id,
                IdeaModel.id == IdeaHistoryModel.idea_id,
                IdeaHistoryModel.idea_status_id == status_id,
                IdeaHistoryModel.is_current_status,
            )
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def find_by_department(
        self, department_id: int
    ) -> Sequence[IdeaModel]:
        session = db_session.get()
        query = select(IdeaModel).filter(
            and_(
                IdeaModel.department_id == department_id,
            )
        )
        result = await session.execute(query)
        return result.scalars().all()
