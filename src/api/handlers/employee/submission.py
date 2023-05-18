import asyncio
import datetime

from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.bad_request import BadRequestException
from src.orm.models import IdeaModel, UserIdeaModel, IdeaHistoryModel, IdeaCategoryModel
from src.orm.repositories import (
    IdeaRepository,
    IdeaHistoryRepository,
    StatusRepository,
    DepartmentRepository,
    CategoryRepository,
    IdeaCategoryRepository,
    UserIdeaRepository,
)
from src.orm.repositories.idea_role import IdeaRoleRepository
from src.schemas.enum import IdeaRoleCodeEnum, IdeaStatusCodeEnum
from src.schemas.requests.employee.submission import EmployeeSubmitIdeaRequest
from src.schemas.responses.auth import UserAuthResponse


class SubmitIdeaHandler:
    def __init__(
        self,
        idea_repository: IdeaRepository = Depends(),
        idea_role_repository: IdeaRoleRepository = Depends(),
        user_idea_repository: UserIdeaRepository = Depends(),
        idea_history_repository: IdeaHistoryRepository = Depends(),
        status_repository: StatusRepository = Depends(),
        department_repository: DepartmentRepository = Depends(),
        category_repository: CategoryRepository = Depends(),
        idea_category_repository: IdeaCategoryRepository = Depends(),
    ):
        self.idea_repository = idea_repository
        self.idea_role_repository = idea_role_repository
        self.user_idea_repository = user_idea_repository
        self.idea_history_repository = idea_history_repository
        self.status_repository = status_repository
        self.department_repository = department_repository
        self.category_repository = category_repository
        self.idea_category_repository = idea_category_repository

    async def handle(
        self, submit_idea_schema: EmployeeSubmitIdeaRequest, user_info: UserAuthResponse
    ) -> None:
        if user_info.id in submit_idea_schema.co_authors_ids:
            raise BadRequestException(detail="author can't be co-author")
        # get roles
        gather_chain = [
            self.idea_role_repository.find_by_code(role.value)
            for role in [
                IdeaRoleCodeEnum.IDEA_AUTHOR,
                IdeaRoleCodeEnum.IDEA_COAUTHOR,
            ]
        ]
        gather_chain.append(
            self.status_repository.find_by_code(IdeaStatusCodeEnum.PROPOSED.value)
        )
        result = await asyncio.gather(*gather_chain)
        if not all(result):
            raise ApplicationException(detail="not all results were found")

        # check category
        categories = await self.category_repository.find_active_by_ids(
            submit_idea_schema.categories_ids
        )
        active_categories_ids = {category.id for category in categories}
        if active_categories_ids != submit_idea_schema.categories_ids:
            raise BadRequestException(detail="wrong categories")

        author_role, coauthor_role, applied_status = result

        # create idea
        created_idea = await self.idea_repository.create(
            IdeaModel(
                title=submit_idea_schema.title,
                problem_description=submit_idea_schema.problem_description,
                solution_description=submit_idea_schema.solution_description,
                department_id=submit_idea_schema.department_id,
                created_at=datetime.datetime.utcnow(),
            )
        )
        print("4" * 20)
        # author
        idea_author = UserIdeaModel(
            idea_id=created_idea.id, user_id=user_info.id, idea_role_id=author_role.id
        )
        # co-authors
        idea_co_authors = [
            UserIdeaModel(
                idea_id=created_idea.id,
                user_id=co_author_id,
                idea_role_id=coauthor_role.id,
            )
            for co_author_id in submit_idea_schema.co_authors_ids
        ]
        # call repository
        await self.user_idea_repository.bulk_save([idea_author, *idea_co_authors])

        # creates history
        await self.idea_history_repository.create(
            IdeaHistoryModel(
                idea_id=created_idea.id,
                status_id=applied_status.id,
                created_at=datetime.datetime.utcnow(),
            )
        )

        # links categories to idea
        ideas_categories_relations = [
            IdeaCategoryModel(category_id=category_id, idea_id=created_idea.id)
            for category_id in active_categories_ids
        ]
        await self.idea_category_repository.bulk_save(ideas_categories_relations)
