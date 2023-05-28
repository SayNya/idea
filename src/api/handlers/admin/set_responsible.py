from datetime import datetime

from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.bad_request import BadRequestException
from src.orm.models import IdeaHistoryModel, UserIdeaModel
from src.orm.repositories import (
    DepartmentAdminRepository,
    UserRepository,
    IdeaRepository,
    IdeaStatusRepository,
    IdeaHistoryRepository,
    UserIdeaRepository,
    IdeaRoleRepository,
)
from src.schemas.enum import IdeaStatusCodeEnum, IdeaRoleCodeEnum
from src.schemas.requests.admin.set_responsible import SetResponsibleRequest
from src.schemas.responses.auth import UserAuthResponse


class SetResponsibleHandler:
    def __init__(
        self,
        department_admin_repository: DepartmentAdminRepository = Depends(),
        user_repository: UserRepository = Depends(),
        idea_repository: IdeaRepository = Depends(),
        idea_status_repository: IdeaStatusRepository = Depends(),
        idea_history_repository: IdeaHistoryRepository = Depends(),
        user_idea_repository: UserIdeaRepository = Depends(),
        idea_role_repository: IdeaRoleRepository = Depends(),
    ):
        self.department_admin_repository = department_admin_repository
        self.user_repository = user_repository
        self.idea_repository = idea_repository
        self.idea_status_repository = idea_status_repository
        self.idea_history_repository = idea_history_repository
        self.user_idea_repository = user_idea_repository
        self.idea_role_repository = idea_role_repository

    async def handle(
        self,
        user_info: UserAuthResponse,
        set_responsible_request: SetResponsibleRequest,
    ) -> None:
        department_admin = (
            await self.department_admin_repository.get_department_of_admin(user_info.id)
        )
        if not department_admin:
            raise ApplicationException(detail="user is not department_admin")
        idea = await self.idea_repository.find_with_history(
            set_responsible_request.idea_id
        )
        if idea.histories[0].idea_status.code != IdeaStatusCodeEnum.ACCEPTED:
            raise BadRequestException()
        responsible_user = await self.user_repository.find(
            set_responsible_request.responsible_id
        )
        if not responsible_user:
            raise BadRequestException()
        realisation_status = await self.idea_status_repository.find_by_code(
            IdeaStatusCodeEnum.REALISATION
        )
        if not realisation_status:
            raise ApplicationException()
        responsible_role = await self.idea_role_repository.find_by_code(
            IdeaRoleCodeEnum.IDEA_RESPONSIBLE
        )
        if not responsible_role:
            raise ApplicationException()
        await self.user_idea_repository.create(
            UserIdeaModel(
                idea_id=idea.id,
                user_id=responsible_user.id,
                idea_role_id=responsible_role.id,
            )
        )
        await self.idea_history_repository.create(
            IdeaHistoryModel(
                idea_id=idea.id,
                idea_status_id=realisation_status.id,
                created_at=datetime.utcnow(),
            )
        )
        await self.idea_history_repository.update(
            idea.histories[0].id, updates={"is_current_status": False}
        )
