from src.schemas.base import BaseRequest


class UserCreate(BaseRequest):
    """Проверяет sign-up запрос"""

    username: str
    password: str
