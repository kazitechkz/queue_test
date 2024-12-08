import base64
from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session, selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.order_model import OrderModel
from app.domain.models.sap_request_model import SapRequestModel
from app.feature.order.dtos.order_dto import OrderCDTO
from app.feature.sap_request.dto.sap_request_dto import SapRequestCDTO
from app.feature.sap_request.sap_request_service import SapRequestService
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class SapRequestRepository(BaseRepository[SapRequestModel]):
    def __init__(self, db: Session = Depends(get_db)) -> None:
        super().__init__(SapRequestModel, db)

    async def request_to_sap(
        self,
        order: OrderModel,
        sapService: SapRequestService,
    ) -> SapRequestModel:
        try:
            sap_request_data = SapRequestModel(
                order_id=order.id,
                werks=order.factory_sap_id,  # Код завода в SAP
                matnr=order.material_sap_id,  # Код материала в SAP
                kun_name=order.name,  # ФИО физического лица
                iin=order.iin,  # ИИН физ. лица
                quan=order.quan,  # Объем заказа
                price=order.price_with_taxes,  # Цена
                dogovor=order.dogovor,
            )
            sap_request = await self.create(obj=sap_request_data)
            sap_request_dto = SapRequestCDTO.from_orm(sap_request)
            if order.organization_id is not None:
                data = await sapService.request_to_sap_legal(
                    werks=sap_request.werks,
                    matnr=sap_request.matnr,
                    dogovor=sap_request.dogovor,
                )
                # Извлечение данных из JSON
                sap_request_dto.status = data.get("STATUS", "0")
                sap_request_dto.zakaz = data.get("ZAKAZ", None)
                sap_request_dto.text = data.get("TEXT", None)
                pdf_base64 = data.get("PDF", "")
                sap_request_dto.pdf = (
                    base64.b64decode(pdf_base64) if pdf_base64 else None
                )  # Декодирование Base64 в байты
                sap_request_dto.date = (
                    datetime.strptime(data.get("DATE", ""), "%Y-%m-%d").date()
                    if data.get("DATE")
                    else None
                )
                sap_request_dto.time = (
                    datetime.strptime(data.get("TIME", ""), "%H:%M:%S").time()
                    if data.get("TIME")
                    else None
                )
            if order.owner_id is not None:
                data = await sapService.request_to_sap_individual(
                    werks=sap_request.werks,
                    matnr=sap_request.matnr,
                    kun_name=sap_request.kun_name,
                    iin=sap_request.iin,
                    quan=sap_request.quan,
                    price=sap_request.price,
                )
                # Извлечение данных из JSON
                sap_request_dto.status = data.get("STATUS", "")
                sap_request_dto.zakaz = data.get("ZAKAZ", None)
                sap_request_dto.text = data.get("TEXT", None)
                pdf_base64 = data.get("PDF", "")
                sap_request_dto.pdf = (
                    base64.b64decode(pdf_base64) if pdf_base64 else None
                )  # Декодирование Base64 в байты
                sap_request_dto.date = (
                    datetime.strptime(data.get("DATE", ""), "%Y-%m-%d").date()
                    if data.get("DATE")
                    else None
                )
                sap_request_dto.time = (
                    datetime.strptime(data.get("TIME", ""), "%H:%M:%S").time()
                    if data.get("TIME")
                    else None
                )
            if sap_request_dto.status == "0":
                sap_request_dto.is_failed = True
            sap_request_updated = await self.update(obj=sap_request, dto=sap_request_dto)
            return sap_request_updated
        except:
            return None

    async def recreate_sap(
        self,
        order: OrderModel,
        userRDTO: UserRDTOWithRelations,
        orderRepo,
        sapRequestService: SapRequestService,
    ):
        if order is None:
            raise AppExceptionResponse.bad_request(message="Заказ не найден")
        if order.sap_id is not None or order.zakaz:
            raise AppExceptionResponse.bad_request(
                message="Счет на предоплату уже создан"
            )
        if userRDTO.user_type.value == TableConstantsNames.UserLegalTypeValue:
            if order.organization is not None:
                if order.organization.owner_id != userRDTO.id:
                    raise AppExceptionResponse.forbidden(message="Нет доступа к заказу")
            else:
                raise AppExceptionResponse.forbidden(message="Нет доступа к заказу")
        elif order.owner_id != userRDTO.id:
            raise AppExceptionResponse.forbidden(message="Нет доступа к заказу")
        sap_request_existed = await self.request_to_sap(
            order=order, sapService=sapRequestService
        )
        if sap_request_existed is None:
            msg = "При создании sap request произошла ошибка"
            raise AppExceptionResponse.internal_error(msg)
        sap_request = await self.request_to_sap(order=order, sapService=sapRequestService)
        if sap_request is not None and not sap_request.is_failed:
            order.zakaz = sap_request.zakaz
            order.sap_id = sap_request.id
            order.status_id = 3
        else:
            order.status_id = 2

        order = await orderRepo.update(obj=order, dto=OrderCDTO.from_orm(order))
        return await orderRepo.get(
            id=order.id,
            options=[
                selectinload(OrderModel.material),
                selectinload(OrderModel.organization),
                selectinload(OrderModel.factory),
                selectinload(OrderModel.workshop),
                selectinload(OrderModel.kaspi),
                selectinload(OrderModel.sap_request),
            ],
        )
