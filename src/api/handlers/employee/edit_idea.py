import asyncio

from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.bad_request import BadRequestException
from src.exceptions.exceptions.not_found import NotFoundException
from src.orm.models import UserIdeaModel, IdeaCategoryModel
from src.orm.repositories import (
    CategoryRepository,
    DepartmentRepository,
    UserIdeaRepository,
    IdeaCategoryRepository,
    IdeaRepository,
    UserRepository,
)

from src.orm.repositories.idea_role import IdeaRoleRepository
from src.schemas.enum import IdeaStatusCodeEnum, IdeaRoleCodeEnum
from src.schemas.requests.employee.edit_idea import EditIdeaRequest
from src.schemas.responses.auth import UserAuthResponse


class EditIdeaHandler:
    def __init__(
        self,
        idea_repository: IdeaRepository = Depends(),
        user_repository: UserRepository = Depends(),
        department_repository: DepartmentRepository = Depends(),
        employee_idea_repository: UserIdeaRepository = Depends(),
        idea_role_repository: IdeaRoleRepository = Depends(),
        category_repository: CategoryRepository = Depends(),
        idea_category_repository: IdeaCategoryRepository = Depends(),
    ):
        self.idea_repository = idea_repository
        self.user_repository = user_repository
        self.department_repository = department_repository
        self.employee_idea_repository = employee_idea_repository
        self.idea_role_repository = idea_role_repository
        self.category_repository = category_repository
        self.idea_category_repository = idea_category_repository

    async def handle(
        self,
        idea_id: int,
        edit_idea_request: EditIdeaRequest,
        user_info: UserAuthResponse,
    ):
        # validate data
        if user_info.id in edit_idea_request.co_authors_ids:
            raise BadRequestException(detail="author can't be co-author")

        # check idea and status
        idea = await self.idea_repository.find_for_employee(idea_id, user_info.id)
        if not idea:
            raise NotFoundException(detail="idea not found")
        if not idea.histories:
            raise ApplicationException(detail="no current status for idea")
        if idea.histories[0].status.code != IdeaStatusCodeEnum.PROPOSED:
            raise BadRequestException(detail="can't edit idea with current status")

        # check co-authors
        co_authors = await asyncio.gather(
            *[
                self.user_repository.find(user_id)
                for user_id in edit_idea_request.co_authors_ids
            ]
        )
        if not all(co_authors):
            raise BadRequestException(detail="wrong co-authors")

        # check department
        department = await self.department_repository.find(
            edit_idea_request.department_id
        )
        if not department:
            raise BadRequestException(detail="wrong department")

        # check category
        categories = await self.category_repository.find_active_by_ids(
            edit_idea_request.categories_ids
        )
        active_categories_ids = {category.id for category in categories}
        if active_categories_ids != edit_idea_request.categories_ids:
            raise BadRequestException(detail="wrong categories")

        # get current data
        co_author_role = await self.idea_role_repository.find_by_code(
            IdeaRoleCodeEnum.IDEA_COAUTHOR
        )
        if not co_author_role:
            raise ApplicationException(detail="can't find role idea-co-author")
        current_co_authors = await self.employee_idea_repository.find_users_for_idea(
            idea.id,
            [IdeaRoleCodeEnum.IDEA_COAUTHOR],
        )
        current_co_authors_ids = {
            current_co_authors.employee_id for current_co_authors in current_co_authors
        }

        # update idea
        await self.idea_repository.update(
            idea.id,
            {
                "title": edit_idea_request.title,
                "problem_description": edit_idea_request.problem_description,
                "solution_description": edit_idea_request.solution_description,
                "department_id": edit_idea_request.department_id,
            },
        )
        # update users
        await self.employee_idea_repository.bulk_delete_for_idea_by_role_and_user_ids(
            idea.id,
            co_author_role.id,
            current_co_authors_ids - edit_idea_request.co_authors_ids,
        )
        await self.employee_idea_repository.bulk_save(
            [
                UserIdeaModel(
                    idea_id=idea.id,
                    employee_id=employee_id,
                    role_id=co_author_role.id,
                )
                for employee_id in edit_idea_request.co_authors_ids
                - current_co_authors_ids
            ]
        )

        # links categories to idea
        old_categories = await self.idea_category_repository.find_by_idea_id(idea.id)
        old_categories_ids = {category.category_id for category in old_categories}

        categories_for_add = edit_idea_request.categories_ids - old_categories_ids
        categories_for_drop = old_categories_ids - edit_idea_request.categories_ids

        await self.idea_category_repository.bulk_delete_categories(
            list(categories_for_drop), idea.id
        )

        ideas_categories_relations_for_add = [
            IdeaCategoryModel(category_id=category_id, idea_id=idea.id)
            for category_id in categories_for_add
        ]
        await self.idea_category_repository.bulk_save(
            ideas_categories_relations_for_add
        )
