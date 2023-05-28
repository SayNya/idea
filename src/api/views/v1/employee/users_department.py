from fastapi import APIRouter, Depends, status

from src.api.handlers.employee.users_departmnet import UsersDepartmentHandler
from src.api.middlewares import session
from src.api.middlewares.role_checker import PermissionChecker
from src.schemas.enum.system_role import SystemRoleCodeEnum
from src.schemas.responses.auth import UserAuthResponse
from src.schemas.responses.base import BaseUserResponse

router = APIRouter(prefix="/users", tags=["employee"])


@router.get("", response_model=list[BaseUserResponse], status_code=status.HTTP_200_OK)
@session()
async def users(
    users_department_handler: UsersDepartmentHandler = Depends(),
    user_info: UserAuthResponse = Depends(
        PermissionChecker(SystemRoleCodeEnum.EMPLOYEE)
    ),
):
    return await users_department_handler.handle(user_info.department.id)
