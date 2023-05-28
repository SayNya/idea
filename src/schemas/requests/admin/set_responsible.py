from src.schemas.base import BaseRequest


class SetResponsibleRequest(BaseRequest):
    idea_id: int
    responsible_id: int
