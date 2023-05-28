from fastapi import Depends

from src.orm.repositories import IdeaRepository
from src.schemas.responses.employee.idea_details import EmployeeIdeaDetailsResponse


class IdeaDetailsHandler:
    def __init__(
        self,
        idea_repository: IdeaRepository = Depends(),
    ):
        self.idea_repository = idea_repository

    async def handle(self, idea_id: int) -> EmployeeIdeaDetailsResponse:
        idea = await self.idea_repository.find_by_idea_id(idea_id)
        response = EmployeeIdeaDetailsResponse.from_orm(idea)
        return response
