from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.bad_request import BadRequestException
from src.exceptions.exceptions.not_found import NotFoundException
from src.orm.models import (
    CouncilUserModel,
    CouncilModel,
    PollModel,
)
from src.orm.repositories import (
    DepartmentAdminRepository,
    DepartmentRepository,
    SystemRoleRepository,
    CouncilRepository,
    UserRepository,
    CouncilUserRepository,
    IdeaRepository,
    IdeaStatusRepository,
    PollRepository,
    CouncilStatusRepository,
    PollStatusRepository,
)
from src.schemas.enum import IdeaStatusCodeEnum, PollStatusCodeEnum
from src.schemas.enum.council_status import CouncilStatusCodeEnum
from src.schemas.requests.admin.convene_council import ConveneCouncilRequest
from src.schemas.responses.auth import UserAuthResponse


class ConveneCouncilHandler:
    def __init__(
        self,
        council_repository: CouncilRepository = Depends(),
        department_repository: DepartmentRepository = Depends(),
        department_admin_repository: DepartmentAdminRepository = Depends(),
        system_role_repository: SystemRoleRepository = Depends(),
        user_repository: UserRepository = Depends(),
        council_user_repository: CouncilUserRepository = Depends(),
        idea_repository: IdeaRepository = Depends(),
        idea_status_repository: IdeaStatusRepository = Depends(),
        poll_repository: PollRepository = Depends(),
        council_status_repository: CouncilStatusRepository = Depends(),
        poll_status_repository: PollStatusRepository = Depends(),
    ):
        self.council_repository = council_repository
        self.department_repository = department_repository
        self.department_admin_repository = department_admin_repository
        self.system_role_repository = system_role_repository
        self.user_repository = user_repository
        self.council_user_repository = council_user_repository
        self.idea_repository = idea_repository
        self.idea_status_repository = idea_status_repository
        self.poll_repository = poll_repository
        self.council_status_repository = council_status_repository
        self.poll_status_repository = poll_status_repository

    async def handle(
        self,
        user_info: UserAuthResponse,
        convene_council_request: ConveneCouncilRequest,
    ) -> None:
        department_admin = (
            await self.department_admin_repository.get_department_of_admin(user_info.id)
        )
        if not department_admin:
            raise ApplicationException(detail="user is not department_admin")

        voters = await self.user_repository.get_users_by_ids_and_department_id(
            convene_council_request.voting_users_ids, department_admin.department_id
        )
        if len(voters) != len(convene_council_request.voting_users_ids):
            raise BadRequestException(detail="wrong voters")

        active_council = await self.council_repository.find_active_for_admin(
            department_admin.department_id,
        )
        if active_council:
            raise BadRequestException(detail="department have active council")

        default_voters = (
            await self.user_repository.get_default_voting_users_by_department_id(
                department_admin.department_id
            )
        )
        final_voters = set(voters) | set(default_voters)
        accepted_status = await self.idea_status_repository.find_by_code(
            IdeaStatusCodeEnum.ACCEPTED
        )
        if not accepted_status:
            raise ApplicationException()

        approved_ideas = (
            await self.idea_repository.find_accepted_ideas_by_status_and_department(
                accepted_status.id, department_admin.department_id
            )
        )
        if not approved_ideas:
            raise NotFoundException(detail="no approved ideas")

        council_status_created = await self.council_status_repository.find_by_code(
            CouncilStatusCodeEnum.CREATED
        )
        if not council_status_created:
            raise ApplicationException()

        poll_status_blocked = await self.poll_status_repository.find_by_code(
            PollStatusCodeEnum.BLOCKED
        )
        if not poll_status_blocked:
            raise ApplicationException()

        # create council
        created_council = await self.council_repository.create(
            CouncilModel(
                department_id=department_admin.department_id,
                chairman_id=convene_council_request.chairman_id,
                planned_council_start=convene_council_request.planned_council_start,
                council_status_id=council_status_created.id,
            )
        )

        # link voting employees to council
        await self.council_user_repository.bulk_save(
            [
                CouncilUserModel(
                    council_id=created_council.id,
                    user=voting_employee,
                )
                for voting_employee in final_voters
            ]
        )

        # create polls
        await self.poll_repository.bulk_save(
            [
                PollModel(
                    idea_id=idea.id,
                    council_id=created_council.id,
                    poll_status_id=poll_status_blocked.id,
                )
                for idea in approved_ideas
            ]
        )
