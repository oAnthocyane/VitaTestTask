"""Роутер для ежедневника"""

import uuid
from fastapi import APIRouter, Path, Query, status
from test_task.apps.diary.schemas import (
    DiaryEntryReadSchema,
    DiaryEntryCreateSchema,
    DiaryEntryUpdateSchema,
    DiaryEntryListResponse,
)
from test_task.apps.diary.depends import (
    GetDiaryEntryUseCaseDep,
    ListDiaryEntriesUseCaseDep,
    CreateDiaryEntryUseCaseDep,
    UpdateDiaryEntryUseCaseDep,
    DeleteDiaryEntryUseCaseDep,
    MarkDiaryEntryCompletedUseCaseDep,
)
from test_task.core.schemas import StatusOkSchema


router = APIRouter(prefix="/api/diary", tags=["Diary"])


@router.post(
    "/", response_model=DiaryEntryReadSchema, status_code=status.HTTP_201_CREATED
)
async def create_diary_entry(
    data: DiaryEntryCreateSchema, use_case: CreateDiaryEntryUseCaseDep
) -> DiaryEntryReadSchema:
    """Создать новую запись в ежедневнике"""
    return await use_case(data)


@router.get("/", response_model=DiaryEntryListResponse)
async def list_diary_entries(
    use_case: ListDiaryEntriesUseCaseDep,
    filter_by: str | None = Query(
        None, description="Фильтр: 'completed', 'pending' или None для всех"
    ),
) -> DiaryEntryListResponse:
    """Получить список записей с опциональной фильтрацией"""
    return await use_case(filter_by)


@router.get("/{entry_id}", response_model=DiaryEntryReadSchema)
async def get_diary_entry(
    use_case: GetDiaryEntryUseCaseDep,
    entry_id: uuid.UUID = Path(..., description="ID записи"),
) -> DiaryEntryReadSchema:
    """Получить запись по ID"""
    return await use_case(entry_id)


@router.put("/{entry_id}", response_model=DiaryEntryReadSchema)
async def update_diary_entry(
    entry_id: uuid.UUID,
    data: DiaryEntryCreateSchema,
    use_case: UpdateDiaryEntryUseCaseDep,
) -> DiaryEntryReadSchema:
    """Обновить запись"""
    update_data = DiaryEntryUpdateSchema(**data.model_dump(exclude={"id"}), id=entry_id)
    return await use_case(update_data)


@router.delete("/{entry_id}", response_model=StatusOkSchema)
async def delete_diary_entry(
    use_case: DeleteDiaryEntryUseCaseDep,
    entry_id: uuid.UUID = Path(..., description="ID записи"),
) -> StatusOkSchema:
    """Удалить запись"""
    await use_case(entry_id)
    return StatusOkSchema()


@router.patch("/{entry_id}/complete", response_model=DiaryEntryReadSchema)
async def mark_diary_entry_completed(
    use_case: MarkDiaryEntryCompletedUseCaseDep,
    entry_id: uuid.UUID = Path(..., description="ID записи"),
) -> DiaryEntryReadSchema:
    """Отметить запись как выполненную"""
    return await use_case(entry_id)
