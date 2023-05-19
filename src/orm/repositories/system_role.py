from sqlalchemy import select

from src.orm.async_database import db_session
from src.orm.models import SystemRoleModel
from src.orm.repositories.base import BaseRepository


class SystemRoleRepository(BaseRepository):
    Model = SystemRoleModel

    async def find_by_code(self, code: str) -> SystemRoleModel:
        session = db_session.get()
        query = select(SystemRoleModel).filter_by(code=code)
        result = await session.execute(query)
        return result.scalars().first()
