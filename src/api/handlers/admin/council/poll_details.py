from fastapi import Depends

from src.exceptions.exceptions.not_found import NotFoundException
from src.orm.repositories import (
    DepartmentAdminsRepository,
    PollRepository,
    VoteRepository,
)
from src.schemas.responses.auth import UserAuthResponse
from src.orm.schemas.responses.responsible.council.acceptance import (
    ResponsiblePollDetailResponse,
)
from src.services.department import mask_as_related_bu


class PollDetailsHandler:
    def __init__(
        self,
        poll_repository: PollRepository = Depends(),
        department_admins_repository: DepartmentAdminsRepository = Depends(),
        vote_repository: VoteRepository = Depends(),
    ):
        self.poll_repository = poll_repository
        self.department_admins_repository = department_admins_repository
        self.vote_repository = vote_repository

    async def handle(
        self, council_id: int, poll_number: int, user_info: UserAuthResponse
    ) -> ResponsiblePollDetailResponse:
        poll = await self.poll_repository.find_for_responsible(
            council_id, poll_number, user_info.id
        )
        if not poll:
            raise NotFoundException(detail="poll not found")
        mask_as_related_bu(poll.idea.business_unit)
        total_polls = await self.poll_repository.count_for_council(council_id)
        votes_count = await self.vote_repository.count_votes_for_poll(
            council_id, poll_number
        )
        schema = ResponsiblePollDetailResponse.from_orm(poll)
        schema.council.total_polls = total_polls
        schema.votes_count = votes_count
        return schema
