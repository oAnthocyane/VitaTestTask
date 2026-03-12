"""Use cases для работы с записями ежедневника"""

import uuid
from typing import Protocol
from test_task.core.use_cases import UseCaseProtocol
from test_task.apps.diary.services.diary_entry import DiaryEntryServiceProtocol
from test_task.apps.diary.schemas import (
    DiaryEntryReadSchema,
    DiaryEntryCreateSchema,
    DiaryEntryUpdateSchema,
    DiaryEntryListResponse,
)


class GetDiaryEntryUseCaseProtocol(UseCaseProtocol[DiaryEntryReadSchema], Protocol):
    async def __call__(self, entry_id: uuid.UUID) -> DiaryEntryReadSchema: ...


class GetDiaryEntryUseCase(GetDiaryEntryUseCaseProtocol):
    """Use case для получения записи"""

    def __init__(self, service: DiaryEntryServiceProtocol):
        self.service = service

    async def __call__(self, entry_id: uuid.UUID) -> DiaryEntryReadSchema:
        return await self.service.get(entry_id)


class ListDiaryEntriesUseCaseProtocol(
    UseCaseProtocol[DiaryEntryListResponse], Protocol
):
    async def __call__(
        self, filter_by: str | None = None
    ) -> DiaryEntryListResponse: ...


class ListDiaryEntriesUseCase(ListDiaryEntriesUseCaseProtocol):
    """Use case для получения списка записей"""

    def __init__(self, service: DiaryEntryServiceProtocol):
        self.service = service

    async def __call__(self, filter_by: str | None = None) -> DiaryEntryListResponse:
        if filter_by == "completed":
            items = await self.service.get_completed()
        elif filter_by == "pending":
            items = await self.service.get_pending()
        else:
            items = await self.service.get_all()

        return DiaryEntryListResponse(items=items, total=len(items))


class CreateDiaryEntryUseCaseProtocol(UseCaseProtocol[DiaryEntryReadSchema], Protocol):
    async def __call__(self, data: DiaryEntryCreateSchema) -> DiaryEntryReadSchema: ...


class CreateDiaryEntryUseCase(CreateDiaryEntryUseCaseProtocol):
    """Use case для создания записи"""

    def __init__(self, service: DiaryEntryServiceProtocol):
        self.service = service

    async def __call__(self, data: DiaryEntryCreateSchema) -> DiaryEntryReadSchema:
        return await self.service.create(data)


class UpdateDiaryEntryUseCaseProtocol(UseCaseProtocol[DiaryEntryReadSchema], Protocol):
    async def __call__(self, data: DiaryEntryUpdateSchema) -> DiaryEntryReadSchema: ...


class UpdateDiaryEntryUseCase(UpdateDiaryEntryUseCaseProtocol):
    """Use case для обновления записи"""

    def __init__(self, service: DiaryEntryServiceProtocol):
        self.service = service

    async def __call__(self, data: DiaryEntryUpdateSchema) -> DiaryEntryReadSchema:
        return await self.service.update(data)


class DeleteDiaryEntryUseCaseProtocol(UseCaseProtocol[None], Protocol):
    async def __call__(self, entry_id: uuid.UUID) -> None: ...


class DeleteDiaryEntryUseCase(DeleteDiaryEntryUseCaseProtocol):
    """Use case для удаления записи"""

    def __init__(self, service: DiaryEntryServiceProtocol):
        self.service = service

    async def __call__(self, entry_id: uuid.UUID) -> None:
        await self.service.delete(entry_id)


class MarkDiaryEntryCompletedUseCaseProtocol(
    UseCaseProtocol[DiaryEntryReadSchema], Protocol
):
    async def __call__(self, entry_id: uuid.UUID) -> DiaryEntryReadSchema: ...


class MarkDiaryEntryCompletedUseCase(MarkDiaryEntryCompletedUseCaseProtocol):
    """Use case для отметки записи как выполненной"""

    def __init__(self, service: DiaryEntryServiceProtocol):
        self.service = service

    async def __call__(self, entry_id: uuid.UUID) -> DiaryEntryReadSchema:
        return await self.service.mark_completed(entry_id)
