"""Репозиторий для работы с записями ежедневника"""

import uuid
from typing import Protocol
import sqlalchemy as sa
from test_task.core.repositories.base_repository import (
    BaseRepositoryImpl,
    BaseRepositoryProtocol,
)
from test_task.apps.diary.models import DiaryEntry
from test_task.apps.diary.schemas import (
    DiaryEntryReadSchema,
    DiaryEntryCreateSchema,
    DiaryEntryUpdateSchema,
)


class DiaryEntryRepositoryProtocol(
    BaseRepositoryProtocol[
        DiaryEntry, DiaryEntryReadSchema, DiaryEntryCreateSchema, DiaryEntryUpdateSchema
    ],
    Protocol,
):
    """Протокол репозитория записей ежедневника"""

    async def mark_as_completed(self, entry_id: uuid.UUID) -> DiaryEntryReadSchema: ...
    async def get_all_completed(self) -> list[DiaryEntryReadSchema]: ...
    async def get_all_pending(self) -> list[DiaryEntryReadSchema]: ...


class DiaryEntryRepository(
    BaseRepositoryImpl[
        DiaryEntry, DiaryEntryReadSchema, DiaryEntryCreateSchema, DiaryEntryUpdateSchema
    ],
    DiaryEntryRepositoryProtocol,
):
    """Реализация репозитория записей ежедневника"""

    async def mark_as_completed(self, entry_id: uuid.UUID) -> DiaryEntryReadSchema:
        """Отметить запись как выполненную"""
        async with self.session as s, s.begin():
            stmt = sa.select(self.model_type).where(self.model_type.id == entry_id)
            result = (await s.execute(stmt)).scalar_one_or_none()

            if not result:
                from test_task.core.utils.exceptions import ModelNotFoundException

                raise ModelNotFoundException(self.model_type, entry_id)

            result.is_completed = True

            return self.read_schema_type.model_validate(result, from_attributes=True)

    async def get_all_completed(self) -> list[DiaryEntryReadSchema]:
        """Получить все выполненные записи"""
        async with self.session as s:
            stmt = (
                sa.select(self.model_type)
                .where(self.model_type.is_completed == True)
                .order_by(self.model_type.created_at.desc())
            )
            result = (await s.execute(stmt)).scalars().all()
            return [
                self.read_schema_type.model_validate(item, from_attributes=True)
                for item in result
            ]

    async def get_all_pending(self) -> list[DiaryEntryReadSchema]:
        """Получить все невыполненные записи"""
        async with self.session as s:
            stmt = (
                sa.select(self.model_type)
                .where(self.model_type.is_completed == False)
                .order_by(self.model_type.created_at.desc())
            )
            result = (await s.execute(stmt)).scalars().all()
            return [
                self.read_schema_type.model_validate(item, from_attributes=True)
                for item in result
            ]
