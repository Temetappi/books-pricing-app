from typing import TypeVar, Generic, Type
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.session = session
        self.model = model

    async def create(self, data_in: CreateSchema) -> ModelType:
        db_obj = self.model(**data_in.model_dump())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, obj_id: int, raise_not_found: bool = True) -> ModelType:
        statement = select(self.model).where(self.model.id == obj_id)
        results = await self.session.execute(statement)
        db_obj = results.scalars().first()
        if not db_obj and raise_not_found:
            raise HTTPException(
                status_code=404, detail=f"Item not found with id {obj_id}"
            )
        return db_obj

    async def update(self, obj_id: int, obj_data: UpdateSchema) -> ModelType:
        db_obj = await self.get_by_id(obj_id=obj_id)
        obj_data_dict = obj_data.model_dump(exclude_unset=True)
        for key, value in obj_data_dict.items():
            setattr(db_obj, key, value)

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)

        return db_obj

    async def delete(self, obj_id: int) -> None:
        db_obj = await self.get_by_id(obj_id=obj_id)
        await self.session.delete(db_obj)
        await self.session.commit()
