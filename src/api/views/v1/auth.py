from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.handlers.auth import RegistrationHandler, AuthorizationHandler
from src.api.middlewares import session
from src.orm.async_database import db_session
from src.schemas.requests.user import UserCreate
from src.schemas.responses.auth import TokenUserResponse

router = APIRouter(prefix="/auth")


@router.post("/sign-up", response_model=TokenUserResponse)
@session()
async def registration(
    user_create: UserCreate,
    registration_handler: RegistrationHandler = Depends(),
):
    return await registration_handler.handle(user_create)


@router.post("/sign-in", response_model=TokenUserResponse)
@session()
async def authorization(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authorization_handler: AuthorizationHandler = Depends(),
):
    return await authorization_handler.handle(form_data)
