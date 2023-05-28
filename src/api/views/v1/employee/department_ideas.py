from fastapi import APIRouter, Depends, status

from src.api.handlers.employee.department_ideas import DepartmentIdeasHandler
from src.api.handlers.employee.my_ideas import MyIdeasHandler
from src.api.middlewares import session
from src.api.middlewares.role_checker import PermissionChecker
from src.schemas.enum.system_role import SystemRoleCodeEnum
from src.schemas.responses.auth import UserAuthResponse
from src.schemas.responses.employee.department_ideas import EmployeeDepartmentIdeasResponse
from src.schemas.responses.employee.my_ideas import EmployeeMyIdeasResponse

router = APIRouter(prefix="/department_ideas", tags=["employee"])


@router.get("", response_model=EmployeeDepartmentIdeasResponse, status_code=status.HTTP_200_OK)
@session()
async def department_ideas(
    department_ideas_handler: DepartmentIdeasHandler = Depends(),
    user_info: UserAuthResponse = Depends(
        PermissionChecker(SystemRoleCodeEnum.EMPLOYEE)
    ),
):
    return await department_ideas_handler.handle(user_info)
