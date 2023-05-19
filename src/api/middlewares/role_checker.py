from fastapi import Depends, status

from src.exceptions.exceptions.auth import UnauthorizedException
from src.schemas.enum.system_role import SystemRoleCodeEnum
from src.schemas.responses.auth import UserAuthResponse
from src.utils.dependecies import get_current_user


class PermissionChecker:
    def __init__(self, required_role: SystemRoleCodeEnum) -> None:
        self.required_role = required_role

    def __call__(
        self, user: UserAuthResponse = Depends(get_current_user)
    ) -> UserAuthResponse:
        for user_role in user.system_roles:
            if self.required_role == user_role.code:
                return user
        raise UnauthorizedException(
            detail=f"Endpoint requires {self.required_role} role"
        )
