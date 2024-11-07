from datetime import datetime
from typing import Optional, List

from fastapi import Depends, UploadFile
from sqlalchemy import and_
from sqlalchemy.orm import Session, selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.core.file_helper import FileUploadHelper
from app.domain.models.order_model import OrderModel
from app.domain.models.payment_document_model import PaymentDocumentModel
from app.feature.order.dtos.order_dto import OrderRDTOWithRelations
from app.feature.order.filter.order_filter import OrderFiltersForPaymentDocuments
from app.feature.order.order_repository import OrderRepository
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class PaymentDocumentRepository(BaseRepository[PaymentDocumentModel]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(PaymentDocumentModel, db)
        self.file_helper = FileUploadHelper(db)

    async def upload_file(self, order_id: int, file: UploadFile, orderRepo: OrderRepository,
                          userRepo: UserRDTOWithRelations):
        if userRepo.user_type.value != TableConstantsNames.UserLegalTypeValue:
            raise AppExceptionResponse.bad_request("Отказано в доступе")
        order: OrderModel = await orderRepo.get(id=order_id)
        if order is None:
            raise AppExceptionResponse.bad_request("Заказ не найден")
        if order.organization_id not in [organization.id for organization in userRepo.organizations]:
            raise AppExceptionResponse.bad_request("Данный заказ не принадлежит вам")
        if order.status_id != 9 and order.status_id != 3:
            raise AppExceptionResponse.bad_request("Данный этап пройден")
        try:
            # Используем FileUploadHelper для сохранения файла и получения записи FileModel
            file_record = await self.file_helper.save_file(file)
        except ValueError as e:
            return {"error": str(e)}

        # Создаем запись PaymentDocumentModel, используя данные из dto и file_record
        document = PaymentDocumentModel(
            file_id=file_record.id,
            order_id=order_id
        )

        # Сохраняем запись в базе данных
        result = await self.create(obj=document)

        return {
            "message": "Файл и платёжный документ успешно загружены",
            "document_id": result.id,
            "file_url": file_record.url
        }

    async def update_order(self, order_id: int, orderRepo: OrderRepository):
        order = await orderRepo.get(id=order_id)
        if order is None:
            raise AppExceptionResponse.bad_request("Заказ не найден")
        order.status_id = 9  # Укажите нужное значение

        # Сохраняем изменения
        await orderRepo.db.commit()
        await orderRepo.db.refresh(order)

    async def get_payment_docs(self,
                               orderRepo: OrderRepository,
                               params: OrderFiltersForPaymentDocuments,
                               userRepo: UserRDTOWithRelations):
        if userRepo.role.value != TableConstantsNames.RoleAccountantValue:
            raise AppExceptionResponse.bad_request("Отказано в доступе")
        return await orderRepo.paginate_with_filter(dto=OrderRDTOWithRelations,
                                                    page=params.page,
                                                    per_page=params.per_page,
                                                    filters=params.apply(userRepo),
                                                    options=[
                                                        selectinload(orderRepo.model.material),
                                                        selectinload(orderRepo.model.organization),
                                                        selectinload(orderRepo.model.factory),
                                                        selectinload(orderRepo.model.workshop),
                                                        selectinload(orderRepo.model.kaspi),
                                                        selectinload(orderRepo.model.sap_request),
                                                    ]
                                                    )

    async def get_payment_doc_by_order(self, order_id: int, orderRepo: OrderRepository):
        order = await orderRepo.get(id=order_id)
        if order is None:
            raise AppExceptionResponse.bad_request("Заказ не найден")
        docs = await self.get_all_with_filter(
            filters=[and_(self.model.order_id == order_id)],
            options=[selectinload(self.model.file)]
        )
        if docs is None:
            raise AppExceptionResponse.bad_request("Ничего не найдено")
        return docs

    async def add_comment_to_doc(self, payment_id: int, status: bool,
                                 userRepo: UserRDTOWithRelations, comment: Optional[str]):
        doc: PaymentDocumentModel = await self.get(id=payment_id)
        if doc is None:
            raise AppExceptionResponse.bad_request("Документ не найден")
        if status is True:
            doc.checked_by = userRepo.id
            doc.checked_at = datetime.now()
            doc.status = True
            if comment is not None:
                doc.comment = comment
        else:
            if comment is not None:
                doc.comment = comment
            doc.checked_by = userRepo.id
            doc.checked_at = datetime.now()
            doc.status = False
        # Сохраняем изменения
        await self.db.commit()
        await self.db.refresh(doc)

        return doc

    async def make_decision(self, order_id: int, orderRepo: OrderRepository, userRepo: UserRDTOWithRelations,
                            status: bool):
        order: OrderModel = await orderRepo.get(id=order_id)
        if order is None:
            raise AppExceptionResponse.bad_request("Заказ не найден")
        if order.checked_payment_by_id is not None:
            raise AppExceptionResponse.bad_request("Решение уже принято")
        if order.status_id == 9 and order.is_paid is False:
            if status is True:
                return await self.accept_doc(order=order, userRepo=userRepo)
            else:
                return await self.cancel_doc(order=order, userRepo=userRepo)
        else:
            raise AppExceptionResponse.bad_request("Заказ уже оплачен")

    async def accept_doc(self, order: OrderModel, userRepo: UserRDTOWithRelations) -> OrderModel:
        order.is_paid = True
        order.paid_at = datetime.now()
        order.checked_payment_by_id = userRepo.id
        order.checked_payment_by = userRepo.name
        order.checked_payment_at = datetime.now()
        order.status_id = 5

        # Сохраняем изменения
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def cancel_doc(self, order: OrderModel, userRepo: UserRDTOWithRelations) -> OrderModel:
        order.is_paid = False
        order.is_active = False
        order.is_finished = True
        order.is_failed = True
        order.checked_payment_by_id = userRepo.id
        order.checked_payment_by = userRepo.name
        order.checked_payment_at = datetime.now()
        order.finished_at = datetime.now()
        order.status_id = 8

        # Сохраняем изменения
        await self.db.commit()
        await self.db.refresh(order)
        return order