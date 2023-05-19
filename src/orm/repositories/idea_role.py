from sqlalchemy import select

from src.orm.async_database import db_session
from src.orm.models import IdeaRoleModel
from src.orm.repositories.base import BaseRepository


class IdeaRoleRepository(BaseRepository):
    Model = IdeaRoleModel

    async def find_by_code(self, code: str) -> IdeaRoleModel:
        session = db_session.get()
        query = select(IdeaRoleModel).filter_by(code=code)
        result = await session.execute(query)
        return result.scalars().first()
