from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.bad_request import BadRequestException
from src.exceptions.exceptions.not_found import NotFoundException
from src.orm.models import PollChoicesModel
from src.orm.repositories import (
    DepartmentAdminsRepository,
    PollChoicesRepository,
    PollRepository,
    VoteRepository,
)
from src.orm.schemas.enum import CouncilStatusesEnum, PollStatusesEnum, VoteChoicesEnum
from src.schemas.responses.auth import UserAuthResponse


class ResponsibleEndPollHandler:
    def __init__(
        self,
        poll_repository: PollRepository = Depends(),
        vote_repository: VoteRepository = Depends(),
        poll_choices_repository: PollChoicesRepository = Depends(),
        department_admins_repository: DepartmentAdminsRepository = Depends(),
    ):
        self.poll_repository = poll_repository
        self.vote_repository = vote_repository
        self.poll_choices_repository = poll_choices_repository
        self.department_admins_repository = department_admins_repository

    async def handle(self, council_id: int, poll_number: int, user_info: UserAuthResponse) -> None:
        department_responsible = (
            await self.department_admins_repository.get_department_of_responsible(
                user_info.id
            )
        )
        if not department_responsible:
            raise ApplicationException(detail="user is not department_responsible")
        # check existing of poll
        poll = await self.poll_repository.find_with_council(council_id, poll_number)
        if (
            not poll
            or poll.council.department_id != department_responsible.department_id
        ):
            raise NotFoundException(detail="poll not found")
        if poll.council.status != CouncilStatusesEnum.ONLINE_VOTING:
            raise BadRequestException(
                detail="can't end poll with current council status"
            )
        # check poll status
        if poll.status != PollStatusesEnum.OPENED.value:
            raise BadRequestException(detail="can't end poll with current status")
        # check council status
        if poll.council.status != CouncilStatusesEnum.ONLINE_VOTING.value:
            raise BadRequestException(
                detail="can't end poll for council with current status"
            )
        # end poll
        poll = await self.poll_repository.update(
            poll.id, {"status": PollStatusesEnum.ENDED.value}
        )

        # count votes
        votes = await self.vote_repository.find_all_by_poll_id(poll.id)
        accepts = 0
        declines = 0
        for vote in votes:
            if vote.choice == VoteChoicesEnum.ACCEPT.value:
                accepts += 1
            elif vote.choice == VoteChoicesEnum.DECLINE.value:
                declines += 1

        # save result of poll
        await self.poll_choices_repository.bulk_save(
            [
                PollChoicesModel(
                    poll_id=poll.id, choice=VoteChoicesEnum.ACCEPT.value, amount=accepts
                ),
                PollChoicesModel(
                    poll_id=poll.id,
                    choice=VoteChoicesEnum.DECLINE.value,
                    amount=declines,
                ),
            ]
        )
