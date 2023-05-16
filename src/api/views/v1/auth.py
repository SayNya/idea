from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.handlers.auth import RegistrationHandler
from src.orm.async_database import get_session, db_session

router = APIRouter(prefix="/auth")


@router.post("/sign-up", response_model=...)
async def registration(
    user: ...,
    registration_handler: RegistrationHandler,
    session: AsyncSession = Depends(get_session),
):
    db_session.set(session)
    return await registration_handler.handle()
