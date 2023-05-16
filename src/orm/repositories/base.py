from sqlalchemy import select

from src.orm.async_database import db_session


class BaseRepository:
    Model = None

    def __init__(self):
        self.session = db_session.get()

    async def find_all(self):
        query = select(self.Model)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def find(self, model_id: int):
        query = select(self.Model).filter_by(id=model_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create(self, entity: Model) -> Model:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def update(self, model_id: int, updates: dict) -> Model:
        query = select(self.Model).filter_by(id=model_id)
        result = await self.session.execute(query)
        entity = result.scalars().first()
        for field, data in updates.items():
            setattr(entity, field, data)
        await self.session.flush([entity])
        return entity

    async def delete(self, model_id) -> None:
        query = select(self.Model).filter_by(id=model_id)
        result = await self.session.execute(query)
        entity = result.scalars().first()
        await self.session.delete(entity)
        await self.session.flush()

    async def bulk_save(self, entities: list[Model]) -> list[Model]:
        self.session.add_all(entities)
        await self.session.flush()
        return entities
