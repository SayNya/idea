from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.handlers.base import BaseHandler
from src.exceptions.exceptions.bad_request import BadRequestException
from src.orm.async_database import db_session
from src.orm.models import UserModel, TokenModel
from src.orm.repositories import UserRepository
from src.orm.repositories.token import TokenRepository
from src.schemas.requests.user import UserCreate
from src.schemas.responses.user import UserResponse, TokenBaseResponse
from src.utils.auth import get_random_string, hash_password, validate_password


class AuthorizationHandler(BaseHandler):
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        token_repository: TokenRepository = Depends(),
    ):
        self.user_repository = user_repository
        self.token_repository = token_repository
        super().__init__(repositories=[self.user_repository, self.token_repository])

    async def handle(self, form_data: OAuth2PasswordRequestForm) -> UserResponse:
        user = await self.user_repository.find_by_username(form_data.username)
        if not user:
            raise BadRequestException(detail="Incorrect username or password")

        if not validate_password(
            password=form_data.password, hashed_password=user.password
        ):
            raise BadRequestException(detail="Incorrect username or password")

        token = TokenModel(expires=datetime.now() + timedelta(weeks=2), user_id=user.id)
        token = await self.token_repository.create(token)
        # user_dict["roles"] = [Role(**role_dict.__dict__) for role_dict in user_dict["roles"]]
        return UserResponse(
            id=user.id, username=user.username, token=TokenBaseResponse.from_orm(token)
        )


class RegistrationHandler(BaseHandler):
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        token_repository: TokenRepository = Depends(),
    ):
        self.user_repository = user_repository
        self.token_repository = token_repository
        super().__init__(repositories=[self.user_repository, self.token_repository])

    async def handle(self, user_create: UserCreate) -> UserResponse:
        db_user = await self.user_repository.find_by_username(user_create.username)
        if db_user:
            raise BadRequestException(detail="Username already registered")
        salt = get_random_string()
        hashed_password = hash_password(user_create.password, salt)
        user = UserModel(
            username=user_create.username, password=f"{salt}${hashed_password}"
        )
        user = await self.user_repository.create(user)

        token = TokenModel(expires=datetime.now() + timedelta(weeks=2), user_id=user.id)
        token = await self.token_repository.create(token)

        return UserResponse(
            id=user.id, username=user.username, token=TokenBaseResponse.from_orm(token)
        )
