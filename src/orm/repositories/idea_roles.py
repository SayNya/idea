from sqlalchemy import select

from src.orm.async_database import db_session
from src.orm.models import IdeaRoleModel
from src.orm.repositories.base import BaseRepository


class IdeaRolesRepository(BaseRepository):
    Model = IdeaRoleModel

    async def find_by_code(self, code: str):
        query = select(IdeaRoleModel).filter_by(code=code)
        result = await db_session.get().execute(query)
        return result.scalars().first()
