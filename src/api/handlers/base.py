from src.orm.repositories.base import BaseRepository


class BaseHandler:
    def __init__(self, repositories: list[BaseRepository]):
        self.repositories = repositories

    def set_session_for_repositories(self):
        for rep in self.repositories:
            rep.set_session()
