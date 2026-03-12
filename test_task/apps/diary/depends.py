"""Dependency injection для модуля ежедневника"""

from typing import Annotated
from fastapi import Depends
from test_task.core.db import AsyncSession, get_async_session
from test_task.apps.diary.models import DiaryEntry
from test_task.apps.diary.schemas import (
    DiaryEntryReadSchema,
    DiaryEntryCreateSchema,
    DiaryEntryUpdateSchema,
)
from test_task.apps.diary.repositories.diary_entry import (
    DiaryEntryRepository,
    DiaryEntryRepositoryProtocol,
)
from test_task.apps.diary.services.diary_entry import (
    DiaryEntryService,
    DiaryEntryServiceProtocol,
)
from test_task.apps.diary.use_cases.diary_entry import (
    GetDiaryEntryUseCase,
    GetDiaryEntryUseCaseProtocol,
    ListDiaryEntriesUseCase,
    ListDiaryEntriesUseCaseProtocol,
    CreateDiaryEntryUseCase,
    CreateDiaryEntryUseCaseProtocol,
    UpdateDiaryEntryUseCase,
    UpdateDiaryEntryUseCaseProtocol,
    DeleteDiaryEntryUseCase,
    DeleteDiaryEntryUseCaseProtocol,
    MarkDiaryEntryCompletedUseCase,
    MarkDiaryEntryCompletedUseCaseProtocol,
)


# Repository
def __get_diary_entry_repository(
    session: AsyncSession = Depends(get_async_session),
) -> DiaryEntryRepositoryProtocol:
    return DiaryEntryRepository(session=session)


# Service
def get_diary_entry_service(
    repository: DiaryEntryRepositoryProtocol = Depends(__get_diary_entry_repository),
) -> DiaryEntryServiceProtocol:
    return DiaryEntryService(repository=repository)


# Use Cases
def get_get_diary_entry_use_case(
    service: DiaryEntryServiceProtocol = Depends(get_diary_entry_service),
) -> GetDiaryEntryUseCaseProtocol:
    return GetDiaryEntryUseCase(service=service)


def get_list_diary_entries_use_case(
    service: DiaryEntryServiceProtocol = Depends(get_diary_entry_service),
) -> ListDiaryEntriesUseCaseProtocol:
    return ListDiaryEntriesUseCase(service=service)


def get_create_diary_entry_use_case(
    service: DiaryEntryServiceProtocol = Depends(get_diary_entry_service),
) -> CreateDiaryEntryUseCaseProtocol:
    return CreateDiaryEntryUseCase(service=service)


def get_update_diary_entry_use_case(
    service: DiaryEntryServiceProtocol = Depends(get_diary_entry_service),
) -> UpdateDiaryEntryUseCaseProtocol:
    return UpdateDiaryEntryUseCase(service=service)


def get_delete_diary_entry_use_case(
    service: DiaryEntryServiceProtocol = Depends(get_diary_entry_service),
) -> DeleteDiaryEntryUseCaseProtocol:
    return DeleteDiaryEntryUseCase(service=service)


def get_mark_diary_entry_completed_use_case(
    service: DiaryEntryServiceProtocol = Depends(get_diary_entry_service),
) -> MarkDiaryEntryCompletedUseCaseProtocol:
    return MarkDiaryEntryCompletedUseCase(service=service)


# Type aliases for dependency injection
DiaryEntryServiceDep = Annotated[
    DiaryEntryServiceProtocol, Depends(get_diary_entry_service)
]
GetDiaryEntryUseCaseDep = Annotated[
    GetDiaryEntryUseCaseProtocol, Depends(get_get_diary_entry_use_case)
]
ListDiaryEntriesUseCaseDep = Annotated[
    ListDiaryEntriesUseCaseProtocol, Depends(get_list_diary_entries_use_case)
]
CreateDiaryEntryUseCaseDep = Annotated[
    CreateDiaryEntryUseCaseProtocol, Depends(get_create_diary_entry_use_case)
]
UpdateDiaryEntryUseCaseDep = Annotated[
    UpdateDiaryEntryUseCaseProtocol, Depends(get_update_diary_entry_use_case)
]
DeleteDiaryEntryUseCaseDep = Annotated[
    DeleteDiaryEntryUseCaseProtocol, Depends(get_delete_diary_entry_use_case)
]
MarkDiaryEntryCompletedUseCaseDep = Annotated[
    MarkDiaryEntryCompletedUseCaseProtocol,
    Depends(get_mark_diary_entry_completed_use_case),
]
