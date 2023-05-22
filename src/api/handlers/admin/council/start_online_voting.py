from datetime import datetime
from itertools import product
from typing import Optional

from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.bad_request import BadRequestException
from src.exceptions.exceptions.not_found import NotFoundException
from src.orm.models import VoteModel
from src.orm.repositories import (
    DepartmentAdminRepository,
    PollRepository,
    CouncilRepository,
    CouncilStatusRepository,
    PollStatusRepository,
    VoteRepository,
)
from src.schemas.enum import PollStatusCodeEnum

from src.schemas.enum.council_status import CouncilStatusCodeEnum
from src.schemas.responses.auth import UserAuthResponse


class StartOnlineVotingHandler:
    def __init__(
        self,
        council_repository: CouncilRepository = Depends(),
        poll_repository: PollRepository = Depends(),
        department_admin_repository: DepartmentAdminRepository = Depends(),
        council_status_repository: CouncilStatusRepository = Depends(),
        poll_status_repository: PollStatusRepository = Depends(),
        vote_repository: VoteRepository = Depends(),
        *,
        check_user_info: bool = True,
    ):
        self.council_repository = council_repository
        self.poll_repository = poll_repository
        self.department_admin_repository = department_admin_repository
        self.council_status_repository = council_status_repository
        self.poll_status_repository = poll_status_repository
        self.vote_repository = vote_repository
        self.check_user_info = check_user_info

    async def handle(
        self, council_id: int, user_info: Optional[UserAuthResponse] = None
    ) -> None:
        if self.check_user_info:
            if not user_info:
                raise ApplicationException(detail="user_info is required parameter")
            department_responsible = (
                await self.department_admin_repository.get_department_of_admin(
                    user_info.id
                )
            )
            if not department_responsible:
                raise ApplicationException(detail="user is not department_admin")
        else:
            department_responsible = None
        # check existing of council
        council = await self.council_repository.find_with_department(council_id)
        if not council or (
            self.check_user_info
            and council.department_id != department_responsible.department_id
        ):
            raise NotFoundException(detail="Council not found")
        # check council status
        if council.council_status.code != CouncilStatusCodeEnum.CREATED:
            raise BadRequestException(
                detail="Cant start online voting for council with current status"
            )
        council_online_voting_status = (
            await self.council_status_repository.find_by_codes(
                [CouncilStatusCodeEnum.ONLINE_VOTING]
            )
        )
        if not council_online_voting_status:
            raise ApplicationException()
        council_online_voting_status = council_online_voting_status[0]
        await self.council_repository.update(
            council.id,
            {
                "council_status_id": council_online_voting_status.id,
                "council_start": datetime.utcnow(),
            },
        )
        polls = await self.poll_repository.find_by_council_id(council.id)
        print(polls)
        print(polls)
        poll_active_status = await self.poll_status_repository.find_by_code(
            PollStatusCodeEnum.OPENED
        )
        if not poll_active_status:
            raise ApplicationException()
        await self.poll_repository.bulk_update(
            [poll.id for poll in polls], poll_status_id=poll_active_status.id
        )
        await self.vote_repository.bulk_save(
            [
                VoteModel(user_id=user.id, poll_id=poll.id, choice=None)
                for user, poll in product(council.users, council.polls)
            ]
        )
