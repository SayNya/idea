from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.orm.async_database import db_session

ModelType = TypeVar("ModelType")


class BaseRepository:
    Model: ModelType = None

    async def find_all(self):
        session = db_session.get()
        query = select(self.Model)
        res = await session.session.execute(query)
        return res.scalars().all()

    async def find(self, model_id: int):
        session = db_session.get()
        query = select(self.Model).filter_by(id=model_id)
        result = await session.execute(query)
        return result.scalars().first()

    async def create(self, entity: ModelType) -> ModelType:
        session = db_session.get()
        session.add(entity)
        await session.commit()
        await session.refresh(entity)
        return entity

    async def update(self, model_id: int, updates: dict) -> Model:
        session = db_session.get()
        query = select(self.Model).filter_by(id=model_id)
        result = await session.execute(query)
        entity = result.scalars().first()
        for field, data in updates.items():
            setattr(entity, field, data)
        await session.flush([entity])
        return entity

    async def delete(self, model_id) -> None:
        session = db_session.get()
        query = select(self.Model).filter_by(id=model_id)
        result = await session.execute(query)
        entity = result.scalars().first()
        await session.delete(entity)
        await session.flush()

    async def bulk_save(self, entities: list[Model]) -> list[Model]:
        session = db_session.get()
        db_session.get().add_all(entities)
        await session.flush()
        return entities
