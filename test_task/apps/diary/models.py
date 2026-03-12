"""Модели для ежедневника"""

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from test_task.core.db import Base
from test_task.core.models import TimestampMixin


class DiaryEntry(TimestampMixin, Base):
    """Модель записи в ежедневнике"""

    __tablename__ = "diary_entries"

    title: Mapped[str] = mapped_column(sa.String(255), nullable=False, index=True)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    is_completed: Mapped[bool] = mapped_column(
        sa.Boolean, default=False, nullable=False, index=True
    )
