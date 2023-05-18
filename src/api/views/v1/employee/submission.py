"""from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.handlers.employee.submission import SubmitIdeaHandler

from src.orm.async_database import db_session, get_session
from src.schemas.responses.user import UserResponse
from src.utils.dependecies import get_current_user

router = APIRouter(prefix="/submission", tags=["employee"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def submit_idea_by_employee(
    # submit_idea_schema: EmployeeSubmitIdeaRequest,
    user_info: UserResponse = Depends(get_current_user),
    submit_idea_handler: SubmitIdeaHandler = Depends(),
    session: AsyncSession = Depends(get_session),
):
    db_session.set(session)
    submit_idea_handler.set_session_for_repositories()
    await submit_idea_handler.handle({}, user_info)
    return {}
"""
