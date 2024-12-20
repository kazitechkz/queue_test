from fastapi import APIRouter, Depends, Path

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import check_admin
from app.domain.models.role_model import RoleModel
from app.feature.role.dtos.role_dto import RoleCDTO, RoleRDTO
from app.feature.role.role_repository import RoleRepository


class RoleController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/",
            response_model=list[RoleRDTO],
            summary="Список ролей",
            description="Получение списка ролей",
        )(self.get_all)
        self.router.post(
            "/create",
            response_model=RoleRDTO,
            summary="Создать роль",
            description="Создание роли",
        )(self.create)
        self.router.get(
            "/get_by_id/{id}",
            response_model=RoleRDTO,
            summary="Получить роль по уникальному ID",
            description="Получение роли по уникальному идентификатору",
        )(self.get_by_id)
        self.router.put(
            "/update/{id}",
            response_model=RoleRDTO,
            summary="Обновить роль по уникальному идентификатору",
            description="Обновление одной роли",
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            summary="Удалить роль по уникальному идентификатору",
            description="Удаление одной роли",
        )(self.delete)

    async def get_all(
        self,
        repo: RoleRepository = Depends(RoleRepository),
        current_user=Depends(check_admin),
    ):
        result = await repo.get_all()
        return result

    async def get_by_id(
        self,
        id: int = Path(gt=0),
        repo: RoleRepository = Depends(RoleRepository),
        current_user=Depends(check_admin),
    ):
        result = await repo.get(id=id)
        if result is None:
            raise AppExceptionResponse.not_found(message="Роль не найдена")
        return result

    async def create(
        self,
        role_dto: RoleCDTO,
        repo: RoleRepository = Depends(RoleRepository),
        current_user=Depends(check_admin),
    ):
        existed_role = await repo.get_by_unique_value(value=role_dto.value)
        if existed_role is not None:
            raise AppExceptionResponse.bad_request(
                message="Такое значение для роли уже существует"
            )
        role = RoleModel(**role_dto.dict())
        result = await repo.create(obj=role)
        return result

    async def update(
        self,
        role_dto: RoleCDTO,
        id: int = Path(gt=0),
        repo: RoleRepository = Depends(RoleRepository),
        current_user=Depends(check_admin),
    ):
        role = await repo.get(id=id)
        if role is None:
            raise AppExceptionResponse.not_found(message="Роль не найдена")
        existed_role = await repo.get_by_unique_value(value=role_dto.value, id=id)
        if existed_role is not None:
            raise AppExceptionResponse.bad_request(
                message="Такое значение для роли уже существует"
            )
        result = await repo.update(obj=role, dto=role_dto)
        return result

    async def delete(
        self,
        id: int = Path(gt=0),
        repo: RoleRepository = Depends(RoleRepository),
        current_user=Depends(check_admin),
    ) -> None:
        await repo.delete(id=id)
