from fastapi import Depends

from src.orm.repositories import IdeaRepository
from src.orm.repositories.idea_role import IdeaRoleRepository
from src.schemas.enum import IdeaRoleCodeEnum
from src.schemas.responses.auth import UserAuthResponse
from src.schemas.responses.employee.department_ideas import EmployeeDepartmentIdeasResponse
from src.schemas.responses.employee.my_ideas import EmployeeMyIdeasResponse


class DepartmentIdeasHandler:
    def __init__(
        self,
        idea_repository: IdeaRepository = Depends(),
        idea_roles_repository: IdeaRoleRepository = Depends(),
    ):
        self.idea_repository = idea_repository
        self.idea_roles_repository = idea_roles_repository

    async def handle(self, user_info: UserAuthResponse) -> EmployeeDepartmentIdeasResponse:
        ideas = await self.idea_repository.find_by_department(user_info.department.id)
        response = EmployeeDepartmentIdeasResponse(ideas=ideas)
        return response
