from fastapi import APIRouter, Depends, status

from src.api.handlers.admin.council import ConveneCouncilHandler
from src.api.middlewares.session import session
from src.schemas.responses.auth import UserAuthResponse

from src.utils.dependecies import get_current_user

router = APIRouter(prefix="/council")


@router.post("", status_code=status.HTTP_201_CREATED)
@session(commit=True)
async def convene_council_by_admin(
    convene_council_request: ConveneCouncilRequest,
    convene_council_handler: ConveneCouncilHandler = Depends(),
    user_info: UserAuthResponse = Depends(get_current_user),
):
    await convene_council_handler.handle(user_info, convene_council_request)
    return {}


@router.get("/history")
@session()
async def councils_history(
    councils_history_param: ResponsibleCouncilsHistoryParam = Depends(
        ResponsibleCouncilsHistoryParam.as_obj
    ),
    councils_history_handler: CouncilsHistoryHandler = Depends(),
    user_info: UserAuthResponse = Depends(get_current_user),
):
    return await councils_history_handler.handle(user_info, councils_history_param)


@router.get("/{council_id}/polls/{poll_number}")
@session()
async def poll_details_by_responsible(
    council_id: int,
    poll_number: int,
    poll_details_handler: PollDetailsHandler = Depends(),
    user_info: UserAuthResponse = Depends(get_current_user),
):
    return await poll_details_handler.handle(council_id, poll_number, user_info)


@router.post("/{council_id}/polls/{poll_number}/end")
@session(commit=True)
async def end_poll_by_responsible(
    council_id: int,
    poll_number: int,
    end_poll_handler: ResponsibleEndPollHandler = Depends(),
    user_info: UserAuthResponse = Depends(get_current_user),
):
    await end_poll_handler.handle(council_id, poll_number, user_info)
    return {}


@router.post("/{council_id}/polls/{poll_number}/close")
@session(commit=True)
async def close_poll(
    council_id: int,
    poll_number: int,
    change_status_request: ResponsibleChangeStatusRequest,
    close_poll_handler: ClosePollHandler = Depends(),
    user_info: UserAuthResponse = Depends(get_current_user),
):
    return await close_poll_handler.handle(
        council_id, poll_number, change_status_request, user_info
    )


@router.get("/{council_id}")
@session()
async def get_council_details_by_responsible(
    council_id: int,
    council_details_handler: CouncilDetailsHandler = Depends(),
    user_info: UserAuthResponse = Depends(get_current_user),
):
    return await council_details_handler.handle(council_id, user_info)


@router.get("/{council_id}/results")
@session()
async def council_results(
    council_id: int,
    council_results_param: CouncilResultsParam = Depends(CouncilResultsParam.as_obj),
    council_results_handler: CouncilResultsHandler = Depends(),
    user_info: UserAuthResponse = Depends(get_current_user),
):
    return await council_results_handler.handle(
        council_id, council_results_param, user_info
    )


@router.post("/{council_id}/start-online-voting")
@session(commit=True)
async def start_online_voting_by_responsible(
    council_id: int,
    start_online_voting_handler: StartOnlineVotingHandler = Depends(),
    user_info: UserAuthResponse = Depends(get_current_user),
):
    await start_online_voting_handler.handle(council_id, user_info)
    return {}


@router.get("/{council_id}/voting-employees")
@session()
async def get_list_of_voting_employees(
    council_id: int,
    council_voting_employees_handle: GetVotingEmployeesHandler = Depends(),
    user_info: UserAuthResponse = Depends(get_current_user),
):
    return await council_voting_employees_handle.handle(council_id, user_info)


@router.put("/{council_id}/voting-employees")
@session(commit=True)
async def change_list_of_voting_employees(
    council_id: int,
    request_schema: CouncilVotingEmployeesRequest,
    update_voting_employees_handler: UpdateVotingEmployeesHandler = Depends(),
    user_info: UserAuthResponse = Depends(get_current_user),
):
    await update_voting_employees_handler.handle(council_id, request_schema, user_info)
    return {}


@router.post("/{council_id}/end")
@session(commit=True)
async def end_council_by_responsible(
    council_id: int,
    end_council_handler: ResponsibleEndCouncilHandler = Depends(),
    user_info: UserAuthResponse = Depends(get_current_user),
):
    return await end_council_handler.handle(council_id, user_info)


@router.get("/{council_id}/polls/{poll_number}/votes/count")
@session()
async def get_votes_count(
    council_id: int,
    poll_number: int,
    votes_count_handler: ResponsibleVotesCountHandler = Depends(),
    user_info: UserAuthResponse = Depends(get_current_user),
):
    return await votes_count_handler.handle(council_id, poll_number)