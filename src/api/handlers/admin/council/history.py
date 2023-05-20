from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.orm.repositories import DepartmentAdminsRepository, CouncilRepository
from src.orm.schemas.common.query.paginator.base import LimitOffsetPaginator
from src.orm.schemas.query.responsible.council.acceptance.history import (
    ResponsibleCouncilsHistoryParam,
)
from src.schemas.responses.auth import UserAuthResponse
from src.orm.schemas.responses.responsible.council.history import (
    ResponsibleCouncilsHistoryResponse,
)
from src.services.department import mask_as_related_bu
from src.services.utils.councils import sort_councils_results


class CouncilsHistoryHandler:
    def __init__(
        self,
        council_repository: CouncilRepository = Depends(),
        department_admins_repository: DepartmentAdminsRepository = Depends(),
    ):
        self.council_repository = council_repository
        self.department_admins_repository = department_admins_repository

    async def handle(
        self, user_info: UserAuthResponse, query_params: ResponsibleCouncilsHistoryParam
    ) -> ResponsibleCouncilsHistoryResponse:
        department_responsible = (
            await self.department_admins_repository.get_department_of_responsible(
                user_info.id
            )
        )
        if not department_responsible:
            raise ApplicationException(detail="user is not department_responsible")
        # get data
        filters = query_params.filter_to_dict
        (
            councils,
            total,
        ) = await self.council_repository.find_all_for_history_by_responsible(
            department_responsible.department_id,
            query_params.paginator,
            user_info.id,
            **filters,
        )
        list(map(lambda council: mask_as_related_bu(council.department), councils))
        # update paginator
        if not query_params.paginator:
            paginator = LimitOffsetPaginator(limit=total, offset=0, total=total)
        else:
            paginator = query_params.paginator
            paginator.total = total
        return ResponsibleCouncilsHistoryResponse(
            councils=sort_councils_results(councils), paginator=paginator
        )
