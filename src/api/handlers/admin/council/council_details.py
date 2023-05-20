from fastapi import Depends

from src.exceptions.exceptions.not_found import NotFoundException
from src.orm.repositories import (
    DepartmentAdminsRepository,
    PollRepository,
    CouncilRepository,
    VoteRepository,
)
from src.orm.schemas.enum import PollStatusesEnum
from src.schemas.responses.auth import UserAuthResponse
from src.orm.schemas.responses.responsible.council.acceptance import (
    ResponsibleCouncilResponse,
)
from src.services.department import mask_as_related_bu


class CouncilDetailsHandler:
    def __init__(
        self,
        technical_council_repository: CouncilRepository = Depends(),
        poll_repository: PollRepository = Depends(),
        department_admins_repository: DepartmentAdminsRepository = Depends(),
        vote_repository: VoteRepository = Depends(),
    ):
        self.technical_council_repository = technical_council_repository
        self.poll_repository = poll_repository
        self.department_admins_repository = department_admins_repository
        self.vote_repository = vote_repository

    async def handle(
        self, council_id: int, user_info: UserAuthResponse
    ) -> ResponsibleCouncilResponse:
        council = (
            await self.technical_council_repository.find_with_details_for_responsible(
                council_id, user_info.id
            )
        )
        if not council:
            raise NotFoundException(detail="council not found")
        list(
            map(lambda poll: mask_as_related_bu(poll.idea.business_unit), council.polls)
        )
        total_polls = await self.poll_repository.count_for_council(council_id)
        schema = ResponsibleCouncilResponse.from_orm(council)
        active_polls = list(
            filter(lambda poll: poll.status == PollStatusesEnum.OPENED, council.polls)
        )
        if active_polls:
            schema.votes_count = await self.vote_repository.count_votes_for_poll(
                council_id, active_polls[0].number
            )
        schema.total_polls = total_polls
        return schema
