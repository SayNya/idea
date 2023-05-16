from fastapi import Depends

from src.orm.repositories import UserRepository


class AuthorizationHandler:
    pass


class RegistrationHandler:
    def __init__(self, user_repository: UserRepository = Depends()):
        pass

    def handle(self):
        pass
