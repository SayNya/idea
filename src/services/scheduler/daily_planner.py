from src.api.middlewares.session import session
from src.orm.repositories import (
    DepartmentAdminRepository,
    CouncilRepository,
)
from src.services.scheduler import scheduler
from src.services.scheduler.tasks.admin import start_online_voting_task


@scheduler.task()
@session()
async def plan_councils_starts():
    council_repository = CouncilRepository()
    today_councils = await council_repository.find_for_scheduler()
    for council in today_councils:
        start_online_voting_task.at(council.planned_council_start).do(council.id)


@scheduler.task()
@session(commit=True)
async def remove_role_from_inactive_department():
    department_admin_repository = DepartmentAdminRepository()

    inactive_departments_relationship = (
        await department_admin_repository.get_admins_by_department_status(status=False)
    )

    departments_admins_ids = {}
    for department in inactive_departments_relationship:
        departments_admins_ids[department.department_id] = department.admin_id

    await department_admin_repository.bulk_delete_admins(
        departments_admins_ids.keys(), set(departments_admins_ids.values())
    )
