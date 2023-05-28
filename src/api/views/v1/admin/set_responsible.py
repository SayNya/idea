from fastapi import APIRouter, Depends, status

from src.api.handlers.admin.set_responsible import SetResponsibleHandler
from src.api.middlewares.role_checker import PermissionChecker
from src.api.middlewares.session import session
from src.schemas.enum.system_role import SystemRoleCodeEnum
from src.schemas.requests.admin.set_responsible import SetResponsibleRequest
from src.schemas.responses.auth import UserAuthResponse

router = APIRouter(prefix="/set_responsible")


@router.post("", status_code=status.HTTP_201_CREATED)
@session(commit=True)
async def set_responsible(
    set_responsible_request: SetResponsibleRequest,
    convene_council_handler: SetResponsibleHandler = Depends(),
    user_info: UserAuthResponse = Depends(PermissionChecker(SystemRoleCodeEnum.ADMIN)),
):
    await convene_council_handler.handle(user_info, set_responsible_request)
    return {}
