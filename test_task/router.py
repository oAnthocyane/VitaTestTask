"""
Основной модуль для роутов приложения.
"""

from fastapi import FastAPI
from test_task.apps.diary.router import router as diary_router


def apply_routes(app: FastAPI) -> FastAPI:
    """
    Применяем роуты приложения.
    """
    app.include_router(diary_router)
    return app
