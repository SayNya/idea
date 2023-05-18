from fastapi import Depends

from src.orm.repositories import IdeaRepository
from src.orm.repositories.idea_role import IdeaRoleRepository
from src.schemas.enum import IdeaRoleCodeEnum
from src.schemas.responses.employee.my_ideas import EmployeeMyIdeasResponse


class MyIdeasHandler:
    def __init__(
        self,
        idea_repository: IdeaRepository = Depends(),
        idea_roles_repository: IdeaRoleRepository = Depends(),
    ):
        self.idea_repository = idea_repository
        self.idea_roles_repository = idea_roles_repository

    async def handle(self, user_id: int) -> EmployeeMyIdeasResponse:
        idea_author_role = await self.idea_roles_repository.find_by_code(
            IdeaRoleCodeEnum.IDEA_AUTHOR.value
        )
        idea_coauthor_role = await self.idea_roles_repository.find_by_code(
            IdeaRoleCodeEnum.IDEA_COAUTHOR.value
        )
        role_ids = [idea_author_role.id, idea_coauthor_role.id]
        ideas = await self.idea_repository.find_by_user(user_id, role_ids)
        response = EmployeeMyIdeasResponse(data=ideas)
        return response
