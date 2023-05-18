import datetime
from typing import Optional

from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.bad_request import BadRequestException
from src.exceptions.exceptions.not_found import NotFoundException
from src.orm.repositories import (
    DepartmentAdminsRepository,
    PollRepository,
    TechnicalCouncilRepository,
)
from src.orm.schemas.enum import CouncilStatusesEnum, PollStatusesEnum
from src.schemas.responses.auth import UserAuthResponse


class StartOnlineVotingHandler:
    def __init__(
        self,
        technical_council_repository: TechnicalCouncilRepository = Depends(),
        poll_repository: PollRepository = Depends(),
        department_admins_repository: DepartmentAdminsRepository = Depends(),
        *,
        check_user_info: bool = True,
    ):
        self.technical_council_repository = technical_council_repository
        self.poll_repository = poll_repository
        self.department_admins_repository = department_admins_repository
        self.check_user_info = check_user_info

    async def handle(self, council_id: int, user_info: Optional[User] = None) -> None:
        if self.check_user_info:
            if not user_info:
                raise ApplicationException(detail="user_info is required parameter")
            department_responsible = (
                await self.department_admins_repository.get_department_of_responsible(
                    user_info.id
                )
            )
            if not department_responsible:
                raise ApplicationException(detail="user is not department_responsible")
        else:
            department_responsible = None
        # check existing of council
        council = await self.technical_council_repository.find_with_dpt(council_id)
        if not council or (
            self.check_user_info
            and council.department_id != department_responsible.department_id
        ):
            raise NotFoundException(detail="Council not found")
        # check council status
        if council.status != CouncilStatusesEnum.PRE_VOTING.value:
            raise BadRequestException(
                detail="Cant start online voting for council with current status"
            )
        await self.technical_council_repository.update(
            council.id,
            {
                "status": CouncilStatusesEnum.ONLINE_VOTING.value,
                "council_start": datetime.datetime.utcnow(),
            },
        )
        polls = await self.poll_repository.find_by_council_id(council.id)
        await self.poll_repository.bulk_update(
            [poll.id for poll in polls][1:], status=PollStatusesEnum.BLOCKED.value
        )
