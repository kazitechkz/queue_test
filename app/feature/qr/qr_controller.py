from fastapi import APIRouter, Depends

from app.feature.order.order_repository import OrderRepository


class QrController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get("/get-qr-link/{order_id}")(self.get_qr)

    async def get_qr(self, repo: OrderRepository = Depends(OrderRepository)) -> None:
        pass
