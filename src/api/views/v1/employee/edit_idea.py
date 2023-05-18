from fastapi import APIRouter, Depends, status

from src.api.handlers.employee.edit_idea import EditIdeaHandler
from src.api.middlewares.session import session
from src.schemas.requests.employee.edit_idea import EditIdeaRequest

from src.schemas.responses.auth import UserAuthResponse
from src.utils.dependecies import get_current_user

router = APIRouter(prefix="/edit", tags=["employee"])


@router.put("/{idea_id}", status_code=status.HTTP_200_OK)
@session(commit=True)
async def edit_idea(
    idea_id: int,
    edit_idea_request: EditIdeaRequest,
    edit_idea_handler: EditIdeaHandler = Depends(),
    user_info: UserAuthResponse = Depends(get_current_user),
):
    await edit_idea_handler.handle(idea_id, edit_idea_request, user_info)
    return {}
