from fastapi import APIRouter, Depends

from src.api.handlers.employee.council import (
    ActiveCouncilsHandler,
    CouncilDetailsHandler,
    VoteHandler,
)

from src.api.middlewares import session
from src.api.middlewares.role_checker import PermissionChecker
from src.schemas.enum import SystemRoleCodeEnum
from src.schemas.requests.employee.vote import EmployeeVoteRequest
from src.schemas.responses.auth import UserAuthResponse
from src.schemas.responses.base import BaseCouncilResponse

router = APIRouter(prefix="/council", tags=["employee"])


@router.get("/active")
@session()
async def get_active_councils(
    active_councils_handler: ActiveCouncilsHandler = Depends(),
    user_info: UserAuthResponse = Depends(
        PermissionChecker(SystemRoleCodeEnum.EMPLOYEE)
    ),
) -> list[BaseCouncilResponse]:
    return await active_councils_handler.handle(user_info)


@router.get("/{council_id}")
@session()
async def get_council_details(
    council_id: int,
    council_details_handler: CouncilDetailsHandler = Depends(),
    user_info: UserAuthResponse = Depends(
        PermissionChecker(SystemRoleCodeEnum.EMPLOYEE)
    ),
):
    return await council_details_handler.handle(council_id, user_info)


@router.patch("/polls/{poll_id}/vote")
@session(commit=True)
async def vote_by_employee(
    poll_id: int,
    vote_request: EmployeeVoteRequest,
    vote_handler: VoteHandler = Depends(),
    user_info: UserAuthResponse = Depends(
        PermissionChecker(SystemRoleCodeEnum.EMPLOYEE)
    ),
):
    await vote_handler.handle(poll_id, user_info, vote_request)
    return {}
