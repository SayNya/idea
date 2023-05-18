import datetime

from fastapi import Depends

from src.exceptions.exceptions.bad_request import BadRequestException
from src.exceptions.exceptions.not_found import NotFoundException
from src.orm.models import PollModel, VoteModel
from src.orm.repositories import (
    CouncilEmployeesRepository,
    IdeaRepository,
    PollRepository,
    TechnicalCouncilRepository,
    VoteRepository,
)
from src.orm.schemas.enum import CouncilStatusesEnum, PollStatusesEnum, VoteChoicesEnum
from src.services.scheduler.tasks.responsible.acceptance.start_online_voting import (
    start_online_voting_task,
)


class StartPreVotingHandler:
    def __init__(
        self,
        idea_repository: IdeaRepository = Depends(),
        technical_council_repository: TechnicalCouncilRepository = Depends(),
        poll_repository: PollRepository = Depends(),
        council_employees_repository: CouncilEmployeesRepository = Depends(),
        vote_repository: VoteRepository = Depends(),
    ):
        self.idea_repository = idea_repository
        self.technical_council_repository = technical_council_repository
        self.poll_repository = poll_repository
        self.council_employees_repository = council_employees_repository
        self.vote_repository = vote_repository

    async def handle(self, council_id: int) -> None:
        # check existing of council
        council = await self.technical_council_repository.find_with_dpt(council_id)
        if not council:
            raise NotFoundException(detail="council not found")
        # check council status
        if council.status != CouncilStatusesEnum.CREATED.value:
            raise BadRequestException(
                detail="can't start online voting for council with current status"
            )

        # collect ideas for council
        ideas_for_council = (
            await self.idea_repository.find_for_acceptance_by_responsible(
                council.department_id
            )
        )
        created_polls = await self.poll_repository.bulk_save(
            [
                PollModel(
                    idea_id=idea.id,
                    number=number,
                    council_id=council.id,
                    status=PollStatusesEnum.OPENED.value,
                )
                for idea, number in zip(
                    ideas_for_council, range(1, len(ideas_for_council) + 1)
                )
            ]
        )

        # create votes for employees
        council_employees = await self.council_employees_repository.find_by_council_id(
            council.id
        )
        for created_poll in created_polls:
            await self.vote_repository.bulk_save(
                [
                    VoteModel(
                        poll_id=created_poll.id,
                        employee_id=council_employee.employee_id,
                        choice=VoteChoicesEnum.NO_CHOICE.value,
                    )
                    for council_employee in council_employees
                ]
            )
        await self.technical_council_repository.update(
            council.id, {"status": CouncilStatusesEnum.PRE_VOTING.value}
        )
        # check online voting
        if council.planned_council_start <= datetime.datetime.utcnow():
            # if it already must be opened
            await start_online_voting_task(council.id)
        elif council.planned_council_start.date() == datetime.datetime.utcnow().date():
            # or if it must be opened today
            start_online_voting_task.at(council.planned_council_start).do(council.id)
