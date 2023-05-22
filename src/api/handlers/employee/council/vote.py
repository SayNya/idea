from fastapi import Depends

from src.exceptions.exceptions.bad_request import BadRequestException
from src.exceptions.exceptions.not_found import NotFoundException
from src.orm.repositories import PollRepository, VoteRepository
from src.schemas.enum import PollStatusCodeEnum
from src.schemas.requests.employee.vote import EmployeeVoteRequest
from src.schemas.responses.auth import UserAuthResponse


class VoteHandler:
    def __init__(
        self,
        vote_repository: VoteRepository = Depends(),
        poll_repository: PollRepository = Depends(),
    ):
        self.vote_repository = vote_repository
        self.poll_repository = poll_repository

    async def handle(
        self,
        poll_id: int,
        user_info: UserAuthResponse,
        vote_request: EmployeeVoteRequest,
    ) -> None:
        poll = await self.poll_repository.find_with_status(poll_id)
        if not poll:
            raise NotFoundException(detail="poll not found")
        if poll.poll_status.code != PollStatusCodeEnum.OPENED:
            raise BadRequestException(detail="can't vote to poll with current status")

        await self.vote_repository.update_choice_by_user_and_poll_ids(
            user_info.id, poll.id, vote_request.choice
        )
