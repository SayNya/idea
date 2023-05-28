import datetime

from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.bad_request import BadRequestException
from src.exceptions.exceptions.not_found import NotFoundException
from src.orm.models import IdeaHistoryModel
from src.orm.repositories import (
    IdeaRepository,
    PollRepository,
    CouncilRepository,
    DepartmentAdminRepository,
    CouncilStatusRepository,
    PollStatusRepository,
    IdeaStatusRepository,
    IdeaHistoryRepository,
)
from src.schemas.enum import (
    CouncilStatusCodeEnum,
    PollStatusCodeEnum,
    IdeaStatusCodeEnum,
)
from src.schemas.responses.auth import UserAuthResponse


class AdminEndCouncilHandler:
    def __init__(
        self,
        council_repository: CouncilRepository = Depends(),
        poll_repository: PollRepository = Depends(),
        idea_repository: IdeaRepository = Depends(),
        department_admin_repository: DepartmentAdminRepository = Depends(),
        council_status_repository: CouncilStatusRepository = Depends(),
        poll_status_repository: PollStatusRepository = Depends(),
        idea_status_repository: IdeaStatusRepository = Depends(),
        idea_history_repository: IdeaHistoryRepository = Depends(),
    ):
        self.council_repository = council_repository
        self.poll_repository = poll_repository
        self.idea_repository = idea_repository
        self.department_admin_repository = department_admin_repository
        self.council_status_repository = council_status_repository
        self.poll_status_repository = poll_status_repository
        self.idea_status_repository = idea_status_repository
        self.idea_history_repository = idea_history_repository

    async def handle(self, council_id: int, user_info: UserAuthResponse):
        department_admin = (
            await self.department_admin_repository.get_department_of_admin(user_info.id)
        )
        if not department_admin:
            raise ApplicationException(detail="user is not department_admin")
        # check existing of council
        council = await self.council_repository.find_with_department(council_id)
        if not council or council.department_id != department_admin.department_id:
            raise NotFoundException(detail="council not found")

        # check council status
        online_status = await self.council_status_repository.find_by_code(
            CouncilStatusCodeEnum.ONLINE_VOTING
        )
        if not online_status:
            raise ApplicationException()
        if council.council_status_id != online_status.id:
            raise BadRequestException(detail="can't end council with current status")
        end_status = await self.council_status_repository.find_by_code(
            CouncilStatusCodeEnum.ENDED
        )
        print("1" * 20)
        if not end_status:
            raise ApplicationException()
        # change council status
        await self.council_repository.update(
            council.id,
            {
                "council_status_id": end_status.id,
                "council_end": datetime.datetime.utcnow(),
            },
        )
        print("2" * 20)

        opened_polls = await self.poll_repository.find_by_council_id_and_statuses(
            council.id, [PollStatusCodeEnum.OPENED]
        )

        accepted_idea_ids = []
        declined_idea_ids = []
        for poll in opened_polls:
            vote_summary = 0
            for vote in poll.votes:
                if vote.choice:
                    vote_summary += 1
                else:
                    vote_summary -= 1
            if vote_summary > 0:
                accepted_idea_ids.append(poll.idea_id)
            else:
                declined_idea_ids.append(poll.idea_id)

        poll_ended_status = await self.poll_status_repository.find_by_code(
            PollStatusCodeEnum.ENDED
        )
        if not poll_ended_status:
            raise ApplicationException()
        await self.poll_repository.bulk_update(
            [poll.id for poll in opened_polls],
            poll_status_id=poll_ended_status.id,
        )
        accepted_status = await self.idea_status_repository.find_by_code(
            IdeaStatusCodeEnum.ACCEPTED
        )
        declined_status = await self.idea_status_repository.find_by_code(
            IdeaStatusCodeEnum.DECLINED
        )
        if not accepted_status or not declined_status:
            raise ApplicationException()
        histories = await self.idea_history_repository.find_current_with_idea_ids(
            accepted_idea_ids + declined_idea_ids
        )
        # update history
        for accepted_idea_id in accepted_idea_ids:
            await self.idea_history_repository.create(
                IdeaHistoryModel(
                    idea_id=accepted_idea_id,
                    idea_status_id=accepted_status.id,
                    created_at=datetime.datetime.utcnow(),
                )
            )
        for declined_idea_id in declined_idea_ids:
            await self.idea_history_repository.create(
                IdeaHistoryModel(
                    idea_id=declined_idea_id,
                    idea_status_id=declined_status.id,
                    created_at=datetime.datetime.utcnow(),
                )
            )
        for history in histories:
            await self.idea_history_repository.update(
                history.id, updates={"is_current_status": False}
            )
