"""Схемы для ежедневника"""

import uuid
from pydantic import BaseModel, Field, ConfigDict
from test_task.core.schemas import CreateBaseModel, UpdateBaseModel, TimestampMixin


class DiaryEntryBaseSchema(BaseModel):
    """Базовая схема записи"""

    title: str = Field(..., max_length=255, description="Заголовок записи")
    content: str = Field(..., description="Содержание записи")


class DiaryEntryCreateSchema(DiaryEntryBaseSchema, CreateBaseModel):
    """Схема создания записи"""

    pass


class DiaryEntryUpdateSchema(DiaryEntryBaseSchema, UpdateBaseModel):
    """Схема обновления записи"""

    pass


class DiaryEntryReadSchema(DiaryEntryBaseSchema, TimestampMixin):
    """Схема чтения записи"""

    id: uuid.UUID
    is_completed: bool = Field(default=False, description="Отметка о выполнении")

    model_config = ConfigDict(from_attributes=True)


class DiaryEntryListResponse(BaseModel):
    """Схема списка записей"""

    items: list[DiaryEntryReadSchema]
    total: int
