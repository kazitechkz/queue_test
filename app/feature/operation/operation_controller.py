from typing import List, Optional

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import get_current_user, check_admin
from app.domain.models.operation_model import OperationModel
from app.feature.operation.dtos.operation_dto import OperationRDTO, OperationCDTO, OperationWithRelationRDTO
from app.feature.operation.operation_repository import OperationRepository
from app.feature.role.role_repository import RoleRepository


class OperationController:

    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get(
            "/",
            response_model=List[OperationWithRelationRDTO],
            summary="Список операций",
            description="Получение списка операций с бизнес-логикой"
        )(self.get_all)
        self.router.post(
            "/create",
            response_model=OperationRDTO,
            summary="Создание операции",
            description="Создание операции с бизнес-логикой"
        )(self.create)
        self.router.get(
            "/get/{id}",
            response_model=OperationWithRelationRDTO,
            summary="Получение операции по уникальному идентификатору",
            description="Получение операции по уникальному идентификатору с бизнес-логикой"
        )(self.get_by_id)
        self.router.get(
            "/get-by-value/{value}",
            response_model=OperationWithRelationRDTO,
            summary="Получение операции по значению",
            description="Получение операции по значению с бизнес-логикой"
        )(self.get_by_value)
        self.router.put(
            "/update/{id}",
            response_model=OperationRDTO,
            summary="Обновление операции по уникальному идентификатору",
            description="Обновление операции по уникальному идентификатору с бизнес-логикой"
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            summary="Удаление операции по уникальному идентификатору",
            description="Удаление операции по уникальному идентификатору с бизнес-логикой"
        )(self.delete)

    async def get_all(
            self,
            repo: OperationRepository = Depends(OperationRepository),
            current_user = Depends(get_current_user)
    ):
        result = await repo.get_all_with_filter(
            options=[
                selectinload(repo.model.role),
                selectinload(repo.model.prev_operation),
                selectinload(repo.model.next_operation)
            ])
        result_dto = [OperationWithRelationRDTO.from_orm(resultItem) for resultItem in result]
        return result_dto

    async def get_by_id(
            self,
            id: int = Path(gt=0),
            repo: OperationRepository = Depends(OperationRepository),
            current_user = Depends(get_current_user)
    ):
        result = await repo.get(id=id,
                                options=[
                                    selectinload(repo.model.role),
                                    selectinload(repo.model.prev_operation),
                                    selectinload(repo.model.next_operation)
                                ]
                                )
        if result is None:
            raise AppExceptionResponse.not_found(message="Операции не найдены")

        result_dto = OperationWithRelationRDTO.from_orm(result)
        return result_dto

    async def get_by_value(
            self,
            value: str = Path(),
            repo: OperationRepository = Depends(OperationRepository),
            current_user = Depends(get_current_user)
    ):
        result = await repo.get_filtered(
            filters={"value": value},
            options=[
                selectinload(repo.model.role),
                selectinload(repo.model.prev_operation),
                selectinload(repo.model.next_operation)
            ]
        )

        if result is None:
            raise AppExceptionResponse.not_found(message="Операции не найдены")

        result_dto = OperationWithRelationRDTO.from_orm(result)
        return result_dto

    async def create(
            self,
            dto: OperationCDTO,
            repo: OperationRepository = Depends(OperationRepository),
            roleRepo: RoleRepository = Depends(RoleRepository),
            current_user=Depends(check_admin)
    ):
        role = await self.check_form(dto=dto,repo=repo,roleRepo=roleRepo)
        dto.role_value = role.value
        result = await repo.create(obj=OperationModel(**dto.dict()))
        return result

    async def update(
            self,
            dto: OperationCDTO,
            id: int = Path(gt=0),
            repo: OperationRepository = Depends(OperationRepository),
            roleRepo: RoleRepository = Depends(RoleRepository),
            current_user=Depends(check_admin)
    ):
        role = await self.check_form(dto=dto,repo=repo,roleRepo=roleRepo,id=id)
        existed = await repo.get(id=id)
        if existed is None:
            raise AppExceptionResponse.bad_request(message="Такой операции не существует")
        dto.role_value = role.value
        result = await repo.update(obj=existed,dto=dto)
        return result

    async def delete(self, id: int = Path(gt=0), repo: OperationRepository = Depends(OperationRepository),current_user=Depends(check_admin)):
        await repo.delete(id=id)

    @staticmethod
    async def check_form(
            dto: OperationCDTO,
            repo: OperationRepository,
            roleRepo: RoleRepository,
            id: Optional[int] = None):
        existed = await repo.get_filtered({"value": dto.value})
        if existed is not None:
            if existed.id != id:
                raise AppExceptionResponse.bad_request(message="Такое значение уже существует")
        if dto.prev_id is not None:
            existed_prev = await repo.get_filtered({"prev_id": dto.prev_id})
            if existed_prev is None:
                raise AppExceptionResponse.bad_request(message="Предыдущего этапа не существует")
            else:
                if existed_prev.id == id:
                    raise AppExceptionResponse.bad_request(message="Предыдущий этап не может ссылаться на самого себя")
        if dto.next_id is not None:
            existed_next = await repo.get_filtered({"next_id": dto.next_id})
            if existed_next is None:
                raise AppExceptionResponse.bad_request(message="Следующего этапа не существует")
            else:
                if existed_next.id == id:
                    raise AppExceptionResponse.bad_request(message="Следующий этап не может ссылаться на самого себя")
        role = await roleRepo.get(id=dto.role_id)
        if role is None:
            raise AppExceptionResponse.bad_request(message="Роли не существует")
        return role

