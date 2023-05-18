"""import asyncio
import datetime

from fastapi import Depends

from src.exceptions.exceptions.application import ApplicationException
from src.exceptions.exceptions.bad_request import BadRequestException
from src.orm.repositories import IdeaRepository, SystemRoleRepository, IdeaHistoryRepository, StatusRepository, \
    DepartmentRepository, CategoryRepository, IdeaCategoryRepository


class SubmitIdeaHandler:
    def __init__(
        self,
        idea_repository: IdeaRepository = Depends(),
        system_role_repository: SystemRoleRepository = Depends(),
        employee_idea_repository: UserIdeaRepository = Depends(),
        idea_history_repository: IdeaHistoryRepository = Depends(),
        status_repository: StatusRepository = Depends(),
        department_repository: DepartmentRepository = Depends(),
        category_repository: CategoryRepository = Depends(),
        idea_category_repository: IdeaCategoryRepository = Depends(),
    ):
        self.idea_repository = idea_repository
        self.role_repository = system_role_repository
        self.employee_idea_repository = employee_idea_repository
        self.idea_history_repository = idea_history_repository
        self.status_repository = status_repository
        self.department_repository = department_repository
        self.category_repository = category_repository
        self.idea_category_repository = idea_category_repository

    async def handle(
        self, submit_idea_schema: EmployeeSubmitIdeaRequest, user_info: User
    ) -> None:
        if user_info.id in submit_idea_schema.co_authors_ids:
            raise BadRequestException(detail="author can't be co-author")
        # get roles
        gather_chain = [
            self.role_repository.find_by_code(role.value)
            for role in [
                RolesCodes.IDEA_CREATOR,
                RolesCodes.IDEA_AUTHOR,
                RolesCodes.IDEA_COAUTHOR,
            ]
        ]
        gather_chain.append(
            self.status_repository.find_by_code(IdeaStatusCodeEnum.APPLIED.value)
        )
        result = await asyncio.gather(*gather_chain)
        if not all(result):
            raise ApplicationException(detail="not all results were found")

        # check business unit for existing
        business_unit = await self.department_repository.find(
            submit_idea_schema.business_unit_id
        )
        if not business_unit:
            raise BadRequestException(
                detail="business unit with this id does not exist"
            )
        if business_unit.root is not None:
            raise BadRequestException(detail="business unit is subdivision")
        if submit_idea_schema.department_id:
            department = await self.department_repository.find(
                submit_idea_schema.department_id
            )
            if not department:
                raise BadRequestException(detail="wrong department")
            if department.parent != department.root or not department.root:
                raise BadRequestException(detail="department is not GD-1")
            if department.root != submit_idea_schema.business_unit_id:
                raise BadRequestException(
                    detail="department is not subdivision of business unit"
                )

        # validate replication
        if submit_idea_schema.parent:
            parent_idea = await self.idea_repository.find(submit_idea_schema.parent)
            if parent_idea.parent:
                raise BadRequestException(detail="wrong replication")

        # check category
        categories = await self.category_repository.find_active_by_ids(
            submit_idea_schema.categories_ids
        )
        active_categories_ids = {category.id for category in categories}
        if active_categories_ids != submit_idea_schema.categories_ids:
            raise BadRequestException(detail="wrong categories")

        creator_role, author_role, coauthor_role, applied_status = result

        # create idea
        created_idea = await self.idea_repository.create(
            IdeaModel(
                title=submit_idea_schema.title,
                problem_description=submit_idea_schema.problem_description,
                solution_description=submit_idea_schema.solution_description,
                department_id=submit_idea_schema.department_id,
                other_department=submit_idea_schema.other_department,
                is_in_release=submit_idea_schema.is_in_realise,
                business_unit_id=submit_idea_schema.business_unit_id,
                created_at=datetime.datetime.utcnow(),
                parent=submit_idea_schema.parent,
            )
        )

        # create idea employees
        # creator
        idea_creator = EmployeesIdeasModel(
            idea_id=created_idea.id, employee_id=user_info.id, role_id=creator_role.id
        )
        # author
        idea_author = EmployeesIdeasModel(
            idea_id=created_idea.id, employee_id=user_info.id, role_id=author_role.id
        )
        # co-authors
        idea_co_authors = [
            EmployeesIdeasModel(
                idea_id=created_idea.id,
                employee_id=co_author_id,
                role_id=coauthor_role.id,
            )
            for co_author_id in submit_idea_schema.co_authors_ids
        ]
        # call repository
        await self.employee_idea_repository.bulk_save(
            [idea_creator, idea_author, *idea_co_authors]
        )

        # creates history
        await self.idea_history_repository.create(
            IdeaHistoryModel(
                idea_id=created_idea.id,
                status_id=applied_status.id,
                creator_id=user_info.id,
                created_at=datetime.datetime.utcnow(),
            )
        )

        # links categories to idea
        ideas_categories_relations = [
            IdeaCategoryModel(category_id=category_id, idea_id=created_idea.id)
            for category_id in active_categories_ids
        ]
        await self.idea_category_repository.bulk_save(ideas_categories_relations)
"""
