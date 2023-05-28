from fastapi import APIRouter, Depends, status

from src.api.handlers.admin.council import (
    ConveneCouncilHandler,
    StartOnlineVotingHandler,
)
from src.api.handlers.admin.council.end_council import AdminEndCouncilHandler
from src.api.middlewares.role_checker import PermissionChecker
from src.api.middlewares.session import session
from src.schemas.enum.system_role import SystemRoleCodeEnum
from src.schemas.requests.admin.convene_council import ConveneCouncilRequest
from src.schemas.responses.auth import UserAuthResponse

router = APIRouter(prefix="/council")


@router.post("", status_code=status.HTTP_201_CREATED)
@session(commit=True)
async def convene_council_by_admin(
    convene_council_request: ConveneCouncilRequest,
    convene_council_handler: ConveneCouncilHandler = Depends(),
    user_info: UserAuthResponse = Depends(PermissionChecker(SystemRoleCodeEnum.ADMIN)),
):
    await convene_council_handler.handle(user_info, convene_council_request)
    return {}


# @router.get("/history")
# @session()
# async def councils_history(
#     councils_history_param: ResponsibleCouncilsHistoryParam = Depends(
#         ResponsibleCouncilsHistoryParam.as_obj
#     ),
#     councils_history_handler: CouncilsHistoryHandler = Depends(),
#     user_info: UserAuthResponse = Depends(PermissionChecker(SystemRoleCodeEnum.ADMIN)),
# ):
#     return await councils_history_handler.handle(user_info, councils_history_param)
#


# @router.get("/{council_id}")
# @session()
# async def get_council_details_by_responsible(
#     council_id: int,
#     council_details_handler: CouncilDetailsHandler = Depends(),
#     user_info: UserAuthResponse = Depends(PermissionChecker(SystemRoleCodeEnum.ADMIN)),
# ):
#     return await council_details_handler.handle(council_id, user_info)
#
#
# @router.get("/{council_id}/results")
# @session()
# async def council_results(
#     council_id: int,
#     council_results_param: CouncilResultsParam = Depends(CouncilResultsParam.as_obj),
#     council_results_handler: CouncilResultsHandler = Depends(),
#     user_info: UserAuthResponse = Depends(PermissionChecker(SystemRoleCodeEnum.ADMIN)),
# ):
#     return await council_results_handler.handle(
#         council_id, council_results_param, user_info
#     )
#
#
@router.post("/{council_id}/start-online-voting")
@session(commit=True)
async def start_online_voting_by_admin(
    council_id: int,
    start_online_voting_handler: StartOnlineVotingHandler = Depends(),
    user_info: UserAuthResponse = Depends(PermissionChecker(SystemRoleCodeEnum.ADMIN)),
):
    await start_online_voting_handler.handle(council_id, user_info)
    return {}


@router.post("/{council_id}/end")
@session(commit=True)
async def end_council_by_admin(
    council_id: int,
    end_council_handler: AdminEndCouncilHandler = Depends(),
    user_info: UserAuthResponse = Depends(PermissionChecker(SystemRoleCodeEnum.ADMIN)),
):
    return await end_council_handler.handle(council_id, user_info)


# @router.get("/{council_id}/voting-employees")
# @session()
# async def get_list_of_voting_employees(
#     council_id: int,
#     council_voting_employees_handle: GetVotingEmployeesHandler = Depends(),
#     user_info: UserAuthResponse = Depends(PermissionChecker(SystemRoleCodeEnum.ADMIN)),
# ):
#     return await council_voting_employees_handle.handle(council_id, user_info)
#
#
# @router.put("/{council_id}/voting-employees")
# @session(commit=True)
# async def change_list_of_voting_employees(
#     council_id: int,
#     request_schema: CouncilVotingEmployeesRequest,
#     update_voting_employees_handler: UpdateVotingEmployeesHandler = Depends(),
#     user_info: UserAuthResponse = Depends(PermissionChecker(SystemRoleCodeEnum.ADMIN)),
# ):
#     await update_voting_employees_handler.handle(council_id, request_schema, user_info)
#     return {}
#
#
# @router.get("/{council_id}/polls/{poll_number}/votes/count")
# @session()
# async def get_votes_count(
#     council_id: int,
#     poll_number: int,
#     votes_count_handler: ResponsibleVotesCountHandler = Depends(),
#     user_info: UserAuthResponse = Depends(PermissionChecker(SystemRoleCodeEnum.ADMIN)),
# ):
#     return await votes_count_handler.handle(council_id, poll_number)
