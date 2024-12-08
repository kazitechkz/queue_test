from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI

from app.core.database import init_db
from app.shared.auth import AuthBearer
from app.shared.controllers import (
    include_routers,  # Новый файл для регистрации всех роутеров
)
from app.shared.docs import setup_documentation
from app.shared.roles import assign_roles


# Реализация lifespan для инициализации базы данных
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


# Создаем приложение FastAPI
app = FastAPI(
    title="DIGITAL QUEUE TEST",
    description="Электронно-цифровая очередь",
    version="0.1",
    lifespan=lifespan,
    debug=True,
    dependencies=[Depends(AuthBearer())],
    docs_url=None,  # Отключаем стандартную документацию на /docs
    redoc_url=None,
)

# Включаем все роутеры
include_routers(app)

# Назначаем роли для маршрутов
assign_roles(app)

# Настраиваем страницы с документацией по ролям
setup_documentation(app)

# Запуск сервера
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
