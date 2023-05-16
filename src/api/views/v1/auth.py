from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.handlers.auth import RegistrationHandler, AuthorizationHandler
from src.orm.async_database import get_session, db_session
from src.schemas.requests.user import UserCreate
from src.schemas.responses.user import UserResponse

router = APIRouter(prefix="/auth")


@router.post("/sign-up", response_model=UserResponse)
async def registration(
    user_create: UserCreate,
    registration_handler: RegistrationHandler = Depends(),
    session: AsyncSession = Depends(get_session),
):
    db_session.set(session)
    registration_handler.set_session_for_repositories()
    return await registration_handler.handle(user_create)


@router.post("/sign-in", response_model=UserResponse)
async def authorization(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authorization_handler: AuthorizationHandler = Depends(),
    session: AsyncSession = Depends(get_session),
):
    db_session.set(session)
    authorization_handler.set_session_for_repositories()
    return await authorization_handler.handle(form_data)
