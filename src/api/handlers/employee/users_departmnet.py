from fastapi import Depends

from src.orm.repositories import UserRepository
from src.schemas.responses.base import BaseUserResponse


class UsersDepartmentHandler:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
    ):
        self.user_repository = user_repository

    async def handle(self, department_id: int) -> list[BaseUserResponse]:
        users = await self.user_repository.find_by_department(department_id)
        print(users)
        return [BaseUserResponse.from_orm(user) for user in users]
