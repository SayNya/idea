from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.orm.repositories import CouncilRepository, CouncilStatusRepository

from src.schemas.enum import CouncilStatusCodeEnum
from src.schemas.responses.auth import UserAuthResponse
from src.schemas.responses.base import BaseCouncilResponse


class ActiveCouncilsHandler:
    def __init__(
        self,
        council_repository: CouncilRepository = Depends(),
        council_status_repository: CouncilStatusRepository = Depends(),
    ):
        self.council_repository = council_repository
        self.council_status_repository = council_status_repository

    async def handle(self, user_info: UserAuthResponse) -> list[BaseCouncilResponse]:
        councils = await self.council_repository.find_active_for_employee(
            user_info.id,
            [CouncilStatusCodeEnum.CREATED, CouncilStatusCodeEnum.ONLINE_VOTING],
        )
        return [BaseCouncilResponse.from_orm(council) for council in councils]
