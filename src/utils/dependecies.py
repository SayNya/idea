from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.api.middlewares import session
from src.orm.models import UserModel
from src.orm.repositories import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


@session()
async def get_current_user(
    token: str = Depends(oauth2_scheme), user_repository: UserRepository = Depends()
) -> UserModel:
    user = await user_repository.get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user
