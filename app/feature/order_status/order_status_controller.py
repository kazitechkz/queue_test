from typing import List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import selectinload, joinedload

from app.core.app_exception_response import AppExceptionResponse
from app.feature.order_status.dtos.order_status_dto import OrderStatusRDTO, OrderStatusWithRelationRDTO
from app.feature.order_status.order_status_repository import OrderStatusRepository


class OrderStatusController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/all")(self.get_all)
        self.router.get("/get/{id}")(self.get)
        self.router.get("/get-by-value/{value}")(self.get_by_value)

    async def get_all(self, repo: OrderStatusRepository = Depends(OrderStatusRepository)):
        result = await repo.get_all_with_filter(options=[selectinload(repo.model.prev_status),selectinload(repo.model.next_status)])
        result_dto = [OrderStatusWithRelationRDTO.from_orm(resultItem) for resultItem in result]
        return result_dto

    async def get(self, id: int = Path(gt=0), repo: OrderStatusRepository = Depends(OrderStatusRepository)):
        result = await repo.get(id=id,options=[selectinload(repo.model.prev_status),selectinload(repo.model.next_status)])
        if result is None:
            raise AppExceptionResponse.not_found(message="Статус операции не найден")
        return OrderStatusWithRelationRDTO.from_orm(result)

    async def get_by_value(self, value: str = Path(description="Значение"),
                           repo: OrderStatusRepository = Depends(OrderStatusRepository)):
        result = await repo.get_filtered(filters={"value": value},options=[selectinload(repo.model.prev_status),selectinload(repo.model.next_status)])
        if result is None:
            raise AppExceptionResponse.not_found(message="Статус операции не найден")
        return OrderStatusWithRelationRDTO.from_orm(result)
