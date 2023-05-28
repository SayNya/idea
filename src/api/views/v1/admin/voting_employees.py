
from fastapi import APIRouter, Depends, status

from src.api.handlers.admin.get_default_voters import GetDefaultVotersHandler
from src.api.middlewares.role_checker import PermissionChecker
from src.api.middlewares.session import session
from src.schemas.enum import SystemRoleCodeEnum
from src.schemas.responses.auth import UserAuthResponse
from src.schemas.responses.base import BaseUserResponse

router = APIRouter(prefix="/voting-employees")


@router.get("", status_code=status.HTTP_200_OK)
@session()
async def get_department_voting_employees(
    voting_employees_handler: GetDefaultVotersHandler = Depends(),
    user_info: UserAuthResponse = Depends(PermissionChecker(SystemRoleCodeEnum.ADMIN)),
) -> list[BaseUserResponse]:
    return await voting_employees_handler.handle(user_info)

# TODO: разработать добавление и удаление
@router.put("", status_code=status.HTTP_200_OK)
@session()
async def set_default_voters(
    voting_employees_handler: GetDefaultVotersHandler = Depends(),
    user_info: UserAuthResponse = Depends(PermissionChecker(SystemRoleCodeEnum.ADMIN)),
) -> list[BaseUserResponse]:
    return await voting_employees_handler.handle(user_info)
