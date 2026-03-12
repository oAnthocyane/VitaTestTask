"""Сервис для работы с записями ежедневника"""

import uuid
from typing import Protocol
from test_task.apps.diary.repositories.diary_entry import DiaryEntryRepositoryProtocol
from test_task.apps.diary.schemas import (
    DiaryEntryReadSchema,
    DiaryEntryCreateSchema,
    DiaryEntryUpdateSchema,
)


class DiaryEntryServiceProtocol(Protocol):
    """Протокол сервиса записей ежедневника"""

    async def get(self, entry_id: uuid.UUID) -> DiaryEntryReadSchema: ...
    async def get_all(self) -> list[DiaryEntryReadSchema]: ...
    async def get_completed(self) -> list[DiaryEntryReadSchema]: ...
    async def get_pending(self) -> list[DiaryEntryReadSchema]: ...
    async def create(self, data: DiaryEntryCreateSchema) -> DiaryEntryReadSchema: ...
    async def update(self, data: DiaryEntryUpdateSchema) -> DiaryEntryReadSchema: ...
    async def delete(self, entry_id: uuid.UUID) -> None: ...
    async def mark_completed(self, entry_id: uuid.UUID) -> DiaryEntryReadSchema: ...


class DiaryEntryService(DiaryEntryServiceProtocol):
    """Реализация сервиса записей ежедневника"""

    def __init__(self, repository: DiaryEntryRepositoryProtocol):
        self.repository = repository

    async def get(self, entry_id: uuid.UUID) -> DiaryEntryReadSchema:
        """Получить запись по ID"""
        return await self.repository.get(entry_id)

    async def get_all(self) -> list[DiaryEntryReadSchema]:
        """Получить все записи"""
        return await self.repository.get_all()

    async def get_completed(self) -> list[DiaryEntryReadSchema]:
        """Получить выполненные записи"""
        return await self.repository.get_all_completed()

    async def get_pending(self) -> list[DiaryEntryReadSchema]:
        """Получить невыполненные записи"""
        return await self.repository.get_all_pending()

    async def create(self, data: DiaryEntryCreateSchema) -> DiaryEntryReadSchema:
        """Создать новую запись"""
        return await self.repository.create(data)

    async def update(self, data: DiaryEntryUpdateSchema) -> DiaryEntryReadSchema:
        """Обновить запись"""
        return await self.repository.update(data)

    async def delete(self, entry_id: uuid.UUID) -> None:
        """Удалить запись"""
        await self.repository.delete(entry_id)

    async def mark_completed(self, entry_id: uuid.UUID) -> DiaryEntryReadSchema:
        """Отметить запись как выполненную"""
        return await self.repository.mark_as_completed(entry_id)
