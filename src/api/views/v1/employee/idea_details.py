from fastapi import APIRouter, Depends, status

from src.api.handlers.employee.idea_details import IdeaDetailsHandler
from src.api.handlers.employee.my_ideas import MyIdeasHandler
from src.api.middlewares import session
from src.api.middlewares.role_checker import PermissionChecker
from src.schemas.enum.system_role import SystemRoleCodeEnum
from src.schemas.responses.auth import UserAuthResponse
from src.schemas.responses.employee.idea_details import EmployeeIdeaDetailsResponse
from src.schemas.responses.employee.my_ideas import EmployeeMyIdeasResponse

router = APIRouter(prefix="/idea", tags=["employee"])


@router.get("/{idea_id}", response_model=EmployeeIdeaDetailsResponse, status_code=status.HTTP_200_OK)
@session()
async def idea_details(
        idea_id: int,
        idea_details_handler: IdeaDetailsHandler = Depends(),
        user_info: UserAuthResponse = Depends(
            PermissionChecker(SystemRoleCodeEnum.EMPLOYEE)
        ),
):
    return await idea_details_handler.handle(idea_id)
