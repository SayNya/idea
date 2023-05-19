from itertools import product
from typing import List

from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.bad_request import BadRequestException
from src.exceptions.exceptions.not_found import NotFoundException
from src.orm.models import CouncilEmployeesModel, VoteModel
from src.orm.repositories import (
    CouncilEmployeesRepository,
    DepartmentAdminsRepository,
    PollRepository,
    TechnicalCouncilRepository,
    UserRepository,
    VoteRepository,
)
from src.orm.schemas.enum import CouncilStatusesEnum, VoteChoicesEnum
from src.orm.schemas.requests.responsible.council import CouncilVotingEmployeesRequest
from src.schemas.responses.auth import UserAuthResponse
from src.orm.schemas.responses.base import BaseVotingEmployeeResponse


class GetVotingEmployeesHandler:
    def __init__(
        self,
        technical_council_repository: TechnicalCouncilRepository = Depends(),
        council_employees_repository: CouncilEmployeesRepository = Depends(),
        department_admins_repository: DepartmentAdminsRepository = Depends(),
    ):
        self.technical_council_repository = technical_council_repository
        self.council_employees_repository = council_employees_repository
        self.department_admins_repository = department_admins_repository

    async def handle(
        self, council_id: int, user_info: UserAuthResponse
    ) -> List[BaseVotingEmployeeResponse]:
        department_responsible = (
            await self.department_admins_repository.get_department_of_responsible(
                user_info.id
            )
        )
        if not department_responsible:
            raise ApplicationException(detail="user is not department_responsible")
        # check existing of council
        council = await self.technical_council_repository.find_with_dpt(council_id)
        if not council or council.department_id != department_responsible.department_id:
            raise NotFoundException(detail="Council not found")

        # get data
        council_employees_list = (
            await self.council_employees_repository.find_by_council_id_with_employees(
                council_id
            )
        )
        employees_list = [
            council_employee.employee for council_employee in council_employees_list
        ]
        return [
            BaseVotingEmployeeResponse(
                employee=council_employee,
                is_chairman=council_employee.id == council.chairman_id,
            )
            for council_employee in employees_list
        ]


class UpdateVotingEmployeesHandler:
    def __init__(
        self,
        technical_council_repository: TechnicalCouncilRepository = Depends(),
        council_employees_repository: CouncilEmployeesRepository = Depends(),
        vote_repository: VoteRepository = Depends(),
        poll_repository: PollRepository = Depends(),
        department_admins_repository: DepartmentAdminsRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ):
        self.technical_council_repository = technical_council_repository
        self.council_employees_repository = council_employees_repository
        self.vote_repository = vote_repository
        self.poll_repository = poll_repository
        self.department_admins_repository = department_admins_repository
        self.user_repository = user_repository

    async def handle(
        self,
        council_id: int,
        request_schema: CouncilVotingEmployeesRequest,
        user_info: UserAuthResponse,
    ):
        department_responsible = (
            await self.department_admins_repository.get_department_of_responsible(
                user_info.id
            )
        )
        if not department_responsible:
            raise ApplicationException(detail="user is not department_responsible")

        all_department_admins_ids = set(
            await self.department_admins_repository.get_department_responsible_ids(
                department_responsible.department_id
            )
        )
        if crossing := all_department_admins_ids & set(
            request_schema.voting_employees_ids
        ):
            raise BadRequestException(
                detail={"message": "wrong voters", "votersIds": list(crossing)}
            )
        # check existing of council
        council = await self.technical_council_repository.find_with_dpt(council_id)
        if not council or council.department_id != department_responsible.department_id:
            raise NotFoundException(detail="Council not found")
        if council.status != CouncilStatusesEnum.PRE_VOTING:
            raise BadRequestException(
                detail="can't change voting employees for council with current status"
            )

        # get current employees ids
        council_employees = (
            await self.council_employees_repository.find_by_council_id_with_employees(
                council_id
            )
        )
        council_employees_ids = {
            council_employee.employee_id for council_employee in council_employees
        }
        # get polls ids
        polls = await self.poll_repository.find_by_council_id(council.id)
        polls_ids = [poll.id for poll in polls]
        # delete extra links
        extra_employees_ids = (
            council_employees_ids - request_schema.voting_employees_ids
        )
        await self.council_employees_repository.delete_for_council(
            council.id,
            extra_employees_ids,
        )
        await self.vote_repository.delete_by_employees_ids_and_council_id(
            polls_ids, extra_employees_ids
        )
        # save new links
        new_employees_ids = request_schema.voting_employees_ids - council_employees_ids
        await self.council_employees_repository.bulk_save(
            [
                CouncilEmployeesModel(council_id=council_id, employee_id=employee_id)
                for employee_id in new_employees_ids
            ]
        )
        await self.vote_repository.bulk_save(
            [
                VoteModel(
                    poll_id=poll_id,
                    employee_id=employee_id,
                    choice=VoteChoicesEnum.NO_CHOICE,
                )
                for employee_id, poll_id in product(new_employees_ids, polls_ids)
            ]
        )

        # update chairman
        await self.technical_council_repository.update(
            council_id, {"chairman_id": request_schema.chairman_id}
        )
