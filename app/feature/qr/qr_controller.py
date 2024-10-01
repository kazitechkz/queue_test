from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.domain.models.order_model import OrderModel
from app.feature.order.order_repository import OrderRepository


class QrController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/get-qr-link/{order_id}", )(self.get_qr)

    async def get_qr(
            self,
            order_id: int = Path(gt=0),
            repo: OrderRepository = Depends(OrderRepository)
    ):
        result = await repo.get(id=order_id, options=[
            selectinload(OrderModel.factory),
            selectinload(OrderModel.workshop),
            selectinload(OrderModel.kaspi),
            selectinload(OrderModel.organization),
        ])
        if result is None:
            raise AppExceptionResponse.not_found(message="Заказ не найден")
        return result
