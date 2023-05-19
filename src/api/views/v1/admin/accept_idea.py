from fastapi import APIRouter, Depends, status

from src.api.handlers.admin.accept_idea import AcceptIdeaHandler
from src.api.middlewares import session
from src.api.middlewares.role_checker import PermissionChecker
from src.schemas.enum.system_role import SystemRoleCodeEnum
from src.schemas.requests.admin.accept_idea import AcceptIdeaRequest
from src.schemas.responses.auth import UserAuthResponse

router = APIRouter(prefix="/accept_idea", tags=["admin"])


@router.put(
    "",
    status_code=status.HTTP_200_OK,
)
@session(commit=True)
async def accept_idea_by_admin(
    accept_idea_schema: AcceptIdeaRequest,
    accept_idea_handler: AcceptIdeaHandler = Depends(),
    user_info: UserAuthResponse = Depends(
        PermissionChecker(SystemRoleCodeEnum.ADMIN)
    ),
):
    await accept_idea_handler.handle(accept_idea_schema, user_info)
    return {}
