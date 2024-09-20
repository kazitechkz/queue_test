from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import check_client
from app.domain.models.order_model import OrderModel
from app.feature.order.order_repository import OrderRepository
from app.feature.sap_request.sap_request_repository import SapRequestRepository
from app.feature.sap_request.sap_request_service import SapRequestService
from app.feature.user.dtos.user_dto import UserRDTOWithRelations
from app.shared.database_constants import TableConstantsNames


class SapRequestController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/recreate/{order_id}", )(self.create_sap_request)


    async def create_sap_request(
            self,
            order_id:int = Path(gt=0,description="Идентификатор заказа"),
            userRDTO: UserRDTOWithRelations = Depends(check_client),
            sapRequestRepo:SapRequestRepository = Depends(SapRequestRepository),
            orderRepo:OrderRepository = Depends(OrderRepository),
            sapRequestService:SapRequestService = Depends(SapRequestService),
    ):

        order = await orderRepo.get(id=order_id, options=[selectinload(OrderModel.organization)])
        return await sapRequestRepo.recreate_sap(
            order=order,
            userRDTO=userRDTO,
            orderRepo=orderRepo,
            sapRequestService=sapRequestService

        )