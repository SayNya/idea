from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.orm.repositories import DepartmentAdminRepository, UserRepository
from src.schemas.responses.auth import UserAuthResponse
from src.schemas.responses.base import BaseUserResponse


class GetDefaultVotersHandler:
    def __init__(
        self,
        department_admin_repository: DepartmentAdminRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ):
        self.department_admin_repository = department_admin_repository
        self.user_repository = user_repository

    async def handle(self, user_info: UserAuthResponse) -> list[BaseUserResponse]:
        department_admin = (
            await self.department_admin_repository.get_department_of_admin(
                user_info.id
            )
        )
        if not department_admin:
            raise ApplicationException(detail="user is not department_admin")

        default_voters = await self.user_repository.get_default_voting_users_by_department_id(
            department_admin.department.id
        )
        return [
            BaseUserResponse.from_orm(voting_user)
            for voting_user in default_voters
        ]
