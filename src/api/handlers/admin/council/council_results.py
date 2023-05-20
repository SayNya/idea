from typing import Optional

from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.not_found import NotFoundException
from src.orm.repositories import (
    CouncilResultsRepository,
    DepartmentAdminsRepository,
    PollRepository,
    CouncilRepository,
)
from src.orm.schemas.enum import CouncilResultAttributeKeysEnum, CouncilStatusesEnum
from src.orm.schemas.query.responsible.council.acceptance import CouncilResultsParam
from src.schemas.responses.auth import UserAuthResponse
from src.orm.schemas.responses.responsible.council.acceptance import (
    CouncilResultsResponse,
)
from src.services.department import mask_as_related_bu


class CouncilResultsHandler:
    def __init__(
        self,
        technical_council_repository: CouncilRepository = Depends(),
        council_results_repository: CouncilResultsRepository = Depends(),
        poll_repository: PollRepository = Depends(),
        department_admins_repository: DepartmentAdminsRepository = Depends(),
    ):
        self.technical_council_repository = technical_council_repository
        self.poll_repository = poll_repository
        self.department_admins_repository = department_admins_repository
        self.council_results_repository = council_results_repository

    async def handle(
        self,
        council_id: int,
        council_results_param: CouncilResultsParam,
        user_info: UserAuthResponse,
    ) -> Optional[CouncilResultsResponse]:
        department_responsible = (
            await self.department_admins_repository.get_department_of_responsible(
                user_info.id
            )
        )
        if not department_responsible:
            raise ApplicationException(detail="user is not department_responsible")
        # check existing of council
        council = await self.technical_council_repository.find_with_employees(
            council_id, user_info.id
        )
        if not council or not (
            council.department_id == department_responsible.department_id
            or council.employees
        ):
            raise NotFoundException(detail="council not found")
        if council.status != CouncilStatusesEnum.COMPLETED:
            return
        # get data
        filters = council_results_param.filter_to_dict
        polls = await self.poll_repository.find_for_results_by_responsible(
            council_id=council.id, employee_id=user_info.id, **filters
        )
        list(map(lambda poll: mask_as_related_bu(poll.idea.business_unit), polls))

        return CouncilResultsResponse(
            id=council.id,
            council_end=council.council_end,
            type=council.type,
            polls=polls,
        )
