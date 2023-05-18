import datetime

from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.bad_request import BadRequestException
from src.orm.models import (
    CouncilEmployeesModel,
    CouncilResultsModel,
    EmployeeRoleModel,
    TechnicalCouncilModel,
)
from src.orm.repositories import (
    CouncilEmployeesRepository,
    CouncilResultsRepository,
    DepartmentAdminsRepository,
    DepartmentRepository,
    EmployeeRoleRepository,
    RoleRepository,
    TechnicalCouncilRepository,
    UserRepository,
)
from src.orm.schemas.common.enum.role import RolesCodes
from src.orm.schemas.enum import (
    CouncilResultAttributeKeysEnum,
    CouncilResultsAttributeTypesEnum,
    CouncilStatusesEnum,
)
from src.orm.schemas.requests.responsible.council import ConveneCouncilRequest
from src.schemas.responses.auth import UserAuthResponse
from src.services.scheduler.tasks.responsible.acceptance.start_pre_voting import (
    start_pre_voting_task,
)


class ConveneCouncilHandler:
    def __init__(
        self,
        technical_council_repository: TechnicalCouncilRepository = Depends(),
        department_repository: DepartmentRepository = Depends(),
        council_employees_repository: CouncilEmployeesRepository = Depends(),
        council_results_repository: CouncilResultsRepository = Depends(),
        department_admins_repository: DepartmentAdminsRepository = Depends(),
        employee_role_repository: EmployeeRoleRepository = Depends(),
        role_repository: RoleRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ):
        self.technical_council_repository = technical_council_repository
        self.department_repository = department_repository
        self.council_employees_repository = council_employees_repository
        self.council_results_repository = council_results_repository
        self.department_admins_repository = department_admins_repository
        self.employee_role_repository = employee_role_repository
        self.role_repository = role_repository
        self.user_repository = user_repository

    async def handle(
        self,
        user_info: UserAuthResponse,
        convene_council_request: ConveneCouncilRequest,
    ) -> None:
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
            convene_council_request.voting_employees_ids
        ):
            raise BadRequestException(
                detail={"message": "wrong voters", "votersIds": list(crossing)}
            )

        active_councils = (
            await self.technical_council_repository.find_active_for_responsible(
                department_responsible.department_id,
            )
        )
        if active_councils:
            raise BadRequestException(detail="department have active councils")
        role = await self.role_repository.find_by_code(RolesCodes.IDEA_VOTER.value)
        if not role:
            raise ApplicationException(detail="role not found")
        # create council
        created_council = await self.technical_council_repository.create(
            TechnicalCouncilModel(
                department_id=department_responsible.department_id,
                chairman_id=convene_council_request.chairman_id,
                planned_council_start=convene_council_request.planned_council_start,
                status=CouncilStatusesEnum.CREATED.value,
            )
        )

        # link voting employees to council
        await self.council_employees_repository.bulk_save(
            [
                CouncilEmployeesModel(
                    council_id=created_council.id,
                    employee_id=voting_employee,
                )
                for voting_employee in convene_council_request.voting_employees_ids
            ]
        )
        current_employees_ids_with_role = set(
            await self.employee_role_repository.find_employees_ids_by_role_id(role.id)
        )
        voters_ids = set(convene_council_request.voting_employees_ids)
        await self.employee_role_repository.bulk_save(
            [
                EmployeeRoleModel(employee_id=user_id, role_id=role.id)
                for user_id in voters_ids - current_employees_ids_with_role
            ]
        )
        # create zero results of council
        await self.council_results_repository.bulk_save(
            [
                CouncilResultsModel(
                    council_id=created_council.id,
                    attribute_key=attribute_key,
                    attribute_type=CouncilResultsAttributeTypesEnum.NUMBER.value,
                    result="0",
                )
                for attribute_key in [
                    CouncilResultAttributeKeysEnum.ACCEPTED_IDEAS.value,
                    CouncilResultAttributeKeysEnum.DECLINED_IDEAS.value,
                    CouncilResultAttributeKeysEnum.TO_UPDATING_IDEAS.value,
                ]
            ]
        )
        # check pre-voting
        if (
            created_council.planned_council_start - datetime.timedelta(days=2)
            <= datetime.datetime.utcnow()
        ):
            # if it already must be opened
            await start_pre_voting_task(created_council.id)
        elif (
            created_council.planned_council_start - datetime.timedelta(days=2)
        ).date() == datetime.datetime.utcnow().date():
            # or if it must be opened today
            start_pre_voting_task.at(created_council.planned_council_start).do(
                created_council.id
            )
