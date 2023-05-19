import datetime

from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.bad_request import BadRequestException
from src.orm.models import IdeaHistoryModel
from src.orm.repositories import (
    IdeaRepository,
    IdeaHistoryRepository,
    IdeaStatusRepository,
)
from src.schemas.enum import IdeaStatusCodeEnum
from src.schemas.requests.admin.accept_idea import AcceptIdeaRequest
from src.schemas.responses.auth import UserAuthResponse


class AcceptIdeaHandler:
    def __init__(
        self,
        idea_repository: IdeaRepository = Depends(),
        idea_history_repository: IdeaHistoryRepository = Depends(),
        idea_status_repository: IdeaStatusRepository = Depends(),
    ):
        self.idea_repository = idea_repository
        self.idea_history_repository = idea_history_repository
        self.idea_status_repository = idea_status_repository

    async def handle(
        self, accept_idea_schema: AcceptIdeaRequest, user_info: UserAuthResponse
    ) -> None:
        idea = await self.idea_repository.find(accept_idea_schema.idea_id)
        if not idea:
            raise BadRequestException(detail="idea not found")
        if idea.department_id != user_info.department.id:
            raise BadRequestException()

        current_history = await self.idea_history_repository.find_current_idea_status(
            idea.id
        )
        if current_history.idea_status.code != IdeaStatusCodeEnum.PROPOSED:
            raise BadRequestException(detail="idea must be proposed")

        new_status = await self.idea_status_repository.find_by_code(
            IdeaStatusCodeEnum.ACCEPTED
            if accept_idea_schema.is_accepted
            else IdeaStatusCodeEnum.DECLINED
        )
        if not new_status:
            raise ApplicationException()

        # update history
        await self.idea_history_repository.create(
            IdeaHistoryModel(
                idea_id=idea.id,
                idea_status_id=new_status.id,
                created_at=datetime.datetime.utcnow(),
            )
        )
        await self.idea_history_repository.update(
            current_history.id, updates={"is_current_status": False}
        )
