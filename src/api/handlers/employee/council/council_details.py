from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.not_found import NotFoundException
from src.orm.repositories import CouncilRepository, CouncilStatusRepository

from src.schemas.enum import CouncilStatusCodeEnum
from src.schemas.responses.auth import UserAuthResponse
from src.schemas.responses.employee.council import CouncilDetailsResponse


class CouncilDetailsHandler:
    def __init__(
        self,
        council_repository: CouncilRepository = Depends(),
        council_status_repository: CouncilStatusRepository = Depends(),
    ):
        self.council_repository = council_repository
        self.council_status_repository = council_status_repository

    async def handle(
        self, council_id: int, user_info: UserAuthResponse
    ) -> CouncilDetailsResponse:
        # check existing of council
        council = await self.council_repository.find_with_details(
            council_id, user_info.id
        )
        if not council:
            raise NotFoundException(detail="council not found")
        print(council.polls[0].poll_status)
        return CouncilDetailsResponse.from_orm(council)
