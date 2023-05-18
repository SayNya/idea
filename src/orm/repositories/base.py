from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.orm.async_database import db_session

ModelType = TypeVar("ModelType")


class BaseRepository:
    Model: ModelType = None

    async def find_all(self):
        query = select(self.Model)
        res = await db_session.get().session.execute(query)
        return res.scalars().all()

    async def find(self, model_id: int):
        query = select(self.Model).filter_by(id=model_id)
        result = await db_session.get().execute(query)
        return result.scalars().first()

    async def create(self, entity: ModelType) -> ModelType:
        db_session.get().add(entity)
        await db_session.get().commit()
        await db_session.get().refresh(entity)
        return entity

    async def update(self, model_id: int, updates: dict) -> Model:
        query = select(self.Model).filter_by(id=model_id)
        result = await db_session.get().execute(query)
        entity = result.scalars().first()
        for field, data in updates.items():
            setattr(entity, field, data)
        await db_session.get().flush([entity])
        return entity

    async def delete(self, model_id) -> None:
        query = select(self.Model).filter_by(id=model_id)
        result = await db_session.get().execute(query)
        entity = result.scalars().first()
        await db_session.get().delete(entity)
        await db_session.get().flush()

    async def bulk_save(self, entities: list[Model]) -> list[Model]:
        db_session.get().add_all(entities)
        await db_session.get().flush()
        return entities
