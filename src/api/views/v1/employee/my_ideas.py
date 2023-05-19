from fastapi import APIRouter, Depends, status

from src.api.handlers.employee.my_ideas import MyIdeasHandler
from src.api.middlewares import session
from src.api.middlewares.role_checker import PermissionChecker
from src.schemas.enum.system_role import SystemRoleCodeEnum
from src.schemas.responses.auth import UserAuthResponse
from src.schemas.responses.employee.my_ideas import EmployeeMyIdeasResponse

router = APIRouter(prefix="/my_ideas", tags=["employee"])


@router.get("", response_model=EmployeeMyIdeasResponse, status_code=status.HTTP_200_OK)
@session()
async def my_ideas(
    my_ideas_handler: MyIdeasHandler = Depends(),
    user_info: UserAuthResponse = Depends(
        PermissionChecker(SystemRoleCodeEnum.EMPLOYEE)
    ),
):
    return await my_ideas_handler.handle(user_info.id)
