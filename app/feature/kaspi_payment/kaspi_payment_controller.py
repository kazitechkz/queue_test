from fastapi import APIRouter, Depends

from app.feature.kaspi_payment.kaspi_payment_repository import KaspiPaymentRepository
from app.feature.kaspi_payment.query_parameters.kaspi_payment_check_param import KaspiPaymentCheckParam
from app.feature.kaspi_payment.query_parameters.kaspi_payment_pay_param import KaspiPaymentPayParam
from app.feature.order.order_repository import OrderRepository
from app.feature.sap_request.sap_request_repository import SapRequestRepository


class KaspiPaymentController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/check")(self.check)
        self.router.get("/pay")(self.pay)

    async def check(
            self,
            params:KaspiPaymentCheckParam = Depends(),
            repo:KaspiPaymentRepository = Depends(KaspiPaymentRepository),
            orderRepo: OrderRepository = Depends(OrderRepository),

    ):
        return await repo.check(params,orderRepo)

    async def pay(self,
                  params:KaspiPaymentPayParam = Depends(),
                  repo:KaspiPaymentRepository = Depends(KaspiPaymentRepository),
                  orderRepo: OrderRepository = Depends(OrderRepository),

                  ):
        return await repo.pay(params,orderRepo)