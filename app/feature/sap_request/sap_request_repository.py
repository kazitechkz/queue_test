import base64
from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.order_model import OrderModel
from app.domain.models.sap_request_model import SapRequestModel
from app.feature.order.order_repository import OrderRepository
from app.feature.sap_request.sap_request_service import SapRequestService


class SapRequestRepository(BaseRepository[SapRequestModel]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(SapRequestModel, db)


    async def request_to_sap(
            self,order:OrderModel,
            sapService:SapRequestService = Depends(SapRequestService),
            orderRepo:OrderRepository = Depends(OrderRepository)
    ):
        sap_request_data = SapRequestModel(
            order_id = order.id,
            werks = order.factory_sap_id,  # Код завода в SAP
            matnr = order.material_sap_id, # Код материала в SAP
            kun_name = order.name,  # ФИО физического лица
            iin = order.iin,  # ИИН физ. лица
            quan = order.quan,  # Объем заказа
            price = order.price_with_taxes,  # Цена
            dogovor = order.dogovor
        )
        sap_request = await self.create(obj=sap_request_data)
        if(order.organization_id is not None):
            data = sapService.request_to_sap_legal(werks=sap_request.werks,matnr=sap_request.matnr,dogovor=sap_request.dogovor)
            # Извлечение данных из JSON
            sap_request.status = data.get("STATUS", "")
            sap_request.zakaz = data.get("ZAKAZ", None)
            sap_request.text = data.get("TEXT", None)
            pdf_base64 = data.get("PDF", "")
            sap_request.pdf_bytes = base64.b64decode(pdf_base64) if pdf_base64 else None  # Декодирование Base64 в байты
            sap_request.transfer_date = datetime.strptime(data.get("DATE", ""), "%Y-%m-%d").date() if data.get("DATE") else None
            sap_request.transfer_time = datetime.strptime(data.get("TIME", ""), "%H:%M:%S").time() if data.get("TIME") else None
        if(order.owner_id is not None):
            data = sapService.request_to_sap_individual(werks=sap_request.werks, matnr=sap_request.matnr, kun_name=sap_request.kun_name,iin=sap_request.iin,price=sap_request.price)
            # Извлечение данных из JSON
            sap_request.status = data.get("STATUS", "")
            sap_request.zakaz = data.get("ZAKAZ", None)
            sap_request.text = data.get("TEXT", None)
            pdf_base64 = data.get("PDF", "")
            sap_request.pdf_bytes = base64.b64decode(pdf_base64) if pdf_base64 else None  # Декодирование Base64 в байты
            sap_request.transfer_date = datetime.strptime(data.get("DATE", ""), "%Y-%m-%d").date() if data.get(
                "DATE") else None
            sap_request.transfer_time = datetime.strptime(data.get("TIME", ""), "%H:%M:%S").time() if data.get(
                "TIME") else None


