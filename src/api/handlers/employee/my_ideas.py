from fastapi import Depends

from src.orm.repositories import IdeaRepository, SystemRoleRepository
from src.orm.repositories.idea_roles import IdeaRolesRepository

from src.schemas.enum.idea_role import IdeaRoleEnum
from src.schemas.responses.employee.my_ideas import EmployeeMyIdeasResponse


class MyIdeasHandler:
    def __init__(
        self,
        idea_repository: IdeaRepository = Depends(),
        idea_roles_repository: IdeaRolesRepository = Depends(),
    ):
        self.idea_repository = idea_repository
        self.idea_roles_repository = idea_roles_repository

    async def handle(self, user_id: int)-> EmployeeMyIdeasResponse:
        idea_author_role = await self.idea_roles_repository.find_by_code(
            IdeaRoleEnum.IDEA_AUTHOR.value
        )
        idea_coauthor_role = await self.idea_roles_repository.find_by_code(
            IdeaRoleEnum.IDEA_COAUTHOR.value
        )
        role_ids = [idea_author_role.id, idea_coauthor_role.id]
        print(role_ids)
        ideas = await self.idea_repository.find_by_user(user_id, role_ids)
        print(ideas[0].users[0].idea_roles)
        response = EmployeeMyIdeasResponse(data=ideas)
        return response
