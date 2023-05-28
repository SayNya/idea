from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.exceptions.exceptions.bad_request import BadRequestException
from src.orm.models import UserModel, TokenModel
from src.orm.repositories import UserRepository, TokenRepository
from src.schemas.requests.user import UserCreate
from src.schemas.responses.auth import (
    TokenResponse,
    UserAuthResponse,
    TokenUserResponse,
)
from src.utils.auth import get_random_string, hash_password, validate_password


class AuthorizationHandler:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        token_repository: TokenRepository = Depends(),
    ):
        self.user_repository = user_repository
        self.token_repository = token_repository

    async def handle(self, form_data: OAuth2PasswordRequestForm) -> TokenUserResponse:
        user = await self.user_repository.find_by_username(form_data.username)
        if not user:
            raise BadRequestException(detail="Incorrect username or password")

        if not validate_password(
            password=form_data.password, hashed_password=user.password, salt=user.salt
        ):
            raise BadRequestException(detail="Incorrect username or password")

        token = TokenModel(expires=datetime.now() + timedelta(weeks=2), user_id=user.id)
        token = await self.token_repository.create(token)

        return TokenUserResponse(**user.__dict__, token=TokenResponse.from_orm(token))


class RegistrationHandler:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        token_repository: TokenRepository = Depends(),
    ):
        self.user_repository = user_repository
        self.token_repository = token_repository

    async def handle(self, user_create: UserCreate) -> TokenUserResponse:
        db_user = await self.user_repository.find_by_username(user_create.username)
        if db_user:
            raise BadRequestException(detail="Username already registered")
        salt = get_random_string()
        hashed_password = hash_password(user_create.password, salt)
        user = UserModel(
            username=user_create.username, password=hashed_password, salt=salt
        )
        user = await self.user_repository.create(user)
        user = await self.user_repository.find_by_username(user.username)

        token = TokenModel(expires=datetime.now() + timedelta(weeks=2), user_id=user.id)
        token = await self.token_repository.create(token)

        return TokenUserResponse(**user.__dict__, token=TokenResponse.from_orm(token))
