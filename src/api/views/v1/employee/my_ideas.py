from fastapi import APIRouter, Depends, status

from src.api.handlers.employee.my_ideas import MyIdeasHandler
from src.api.middlewares.session import session
from src.orm.async_database import db_session
from src.schemas.responses.employee.my_ideas import EmployeeMyIdeasResponse
from src.schemas.responses.user import UserResponse
from src.utils.dependecies import get_current_user

router = APIRouter(
    prefix="/my-ideas",
    tags=["employee"],
)


@router.get("", response_model=EmployeeMyIdeasResponse, status_code=status.HTTP_200_OK)
@session()
async def my_ideas(
    # submit_idea_schema: EmployeeSubmitIdeaRequest,
    user_info: UserResponse = Depends(get_current_user),
    my_ideas_handler: MyIdeasHandler = Depends(),
):

    return await my_ideas_handler.handle(user_info.id)
