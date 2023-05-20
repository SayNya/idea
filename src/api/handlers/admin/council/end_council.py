import datetime

from fastapi import Depends

from src.api.handlers.responsible.council.acceptance.council_details import (
    CouncilDetailsHandler,
)
from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.bad_request import BadRequestException
from src.exceptions.exceptions.not_found import NotFoundException
from src.orm.repositories import (
    DepartmentAdminsRepository,
    IdeaRepository,
    PollRepository,
    CouncilRepository,
)
from src.orm.schemas.enum import CouncilStatusesEnum, PollStatusesEnum
from src.schemas.responses.auth import UserAuthResponse
from src.orm.schemas.responses.responsible.council import CompleteCouncilResponse


class ResponsibleEndCouncilHandler:
    def __init__(
        self,
        council_repository: CouncilRepository = Depends(),
        poll_repository: PollRepository = Depends(),
        idea_repository: IdeaRepository = Depends(),
        department_admins_repository: DepartmentAdminsRepository = Depends(),
    ):
        self.council_repository = council_repository
        self.poll_repository = poll_repository
        self.council_details_handler = CouncilDetailsHandler(council_repository)
        self.idea_repository = idea_repository
        self.department_admins_repository = department_admins_repository

    async def handle(
        self, council_id: int, user_info: UserAuthResponse
    ) -> CompleteCouncilResponse:
        department_responsible = (
            await self.department_admins_repository.get_department_of_responsible(
                user_info.id
            )
        )
        if not department_responsible:
            raise ApplicationException(detail="user is not department_responsible")
        # check existing of council
        council = await self.council_repository.find_with_department(council_id)
        if not council or council.department_id != department_responsible.department_id:
            raise NotFoundException(detail="council not found")

        # check council status
        if council.status != CouncilStatusesEnum.ONLINE_VOTING:
            raise BadRequestException(detail="can't end council with current status")
        # change council status
        await self.council_repository.update(
            council.id,
            {
                "status": CouncilStatusesEnum.COMPLETED,
                "council_end": datetime.datetime.utcnow(),
            },
        )
        # update polls
        blocked_polls = await self.poll_repository.find_by_council_id_and_statuses(
            council.id, [PollStatusesEnum.BLOCKED]
        )
        ended_polls = await self.poll_repository.find_by_council_id_and_statuses(
            council.id, [PollStatusesEnum.ENDED]
        )
        opened_polls = await self.poll_repository.find_by_council_id_and_statuses(
            council.id, [PollStatusesEnum.OPENED]
        )
        if blocked_polls or ended_polls or opened_polls:
            await self.idea_repository.bulk_update(
                [poll.idea_id for poll in blocked_polls + ended_polls + opened_polls],
                if_accept_council=False,
            )
            await self.poll_repository.bulk_update(
                [poll.id for poll in blocked_polls + ended_polls + opened_polls],
                status=PollStatusesEnum.CANCELED,
            )
        return CompleteCouncilResponse()
