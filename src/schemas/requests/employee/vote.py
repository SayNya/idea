from src.schemas.base import BaseRequest


class EmployeeVoteRequest(BaseRequest):
    choice: bool
