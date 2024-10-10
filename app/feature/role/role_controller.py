from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Query

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import check_admin
from app.domain.models.role_model import RoleModel
from app.feature.role.dtos.role_dto import RoleRDTO, RoleCDTO
from app.feature.role.role_repository import RoleRepository


class RoleController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/", response_model=List[RoleRDTO])(self.get_all)
        self.router.post("/create", response_model=RoleRDTO)(self.create)
        self.router.get("/get_by_id/{id}", response_model=RoleRDTO)(self.get_by_id)
        self.router.put("/update/{id}", response_model=RoleRDTO)(self.update)
        self.router.delete("/delete/{id}")(self.delete)

    async def get_all(self, repo: RoleRepository = Depends(RoleRepository), current_user=Depends(check_admin)):
        result = await repo.get_all()
        return result

    async def get_by_id(self, id: int = Path(gt=0), repo: RoleRepository = Depends(RoleRepository),current_user=Depends(check_admin)):
        result = await repo.get(id=id)
        if result is None:
            raise AppExceptionResponse.not_found(message="Роль не найдена")
        return result



    async def create(self, role_dto: RoleCDTO, repo: RoleRepository = Depends(RoleRepository),current_user=Depends(check_admin)):
        existed_role = await repo.get_by_unique_value(value=role_dto.value)
        if (existed_role is not None):
            raise AppExceptionResponse.bad_request(message="Такое значение для роли уже существует")
        role = RoleModel(**role_dto.dict())
        result = await repo.create(obj=role)
        return result

    async def update(self, role_dto: RoleCDTO, id: int = Path(gt=0), repo: RoleRepository = Depends(RoleRepository),current_user=Depends(check_admin)):
        role = await repo.get(id=id)
        if role is None:
            raise AppExceptionResponse.not_found(message="Роль не найдена")
        existed_role = await repo.get_by_unique_value(value=role_dto.value, id=id)
        if (existed_role is not None):
            raise AppExceptionResponse.bad_request(message="Такое значение для роли уже существует")
        result = await repo.update(obj=role, dto=role_dto)
        return result

    async def delete(self, id: int = Path(gt=0), repo: RoleRepository = Depends(RoleRepository)):
        await repo.delete(id=id)
