from fastapi import APIRouter, Depends, status

from src.api.handlers.employee.submission import SubmitIdeaHandler
from src.api.middlewares import session
from src.schemas.requests.employee.submission import EmployeeSubmitIdeaRequest
from src.schemas.responses.auth import UserAuthResponse
from src.utils.dependecies import get_current_user

router = APIRouter(prefix="/submission", tags=["employee"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
@session(commit=True)
async def submit_idea_by_employee(
    submit_idea_schema: EmployeeSubmitIdeaRequest,
    submit_idea_handler: SubmitIdeaHandler = Depends(),
    user_info: UserAuthResponse = Depends(get_current_user),
):
    await submit_idea_handler.handle(submit_idea_schema, user_info)
    return {}
