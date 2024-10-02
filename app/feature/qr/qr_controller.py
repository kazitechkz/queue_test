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

            repo: OrderRepository = Depends(OrderRepository)
    ):
        pass
