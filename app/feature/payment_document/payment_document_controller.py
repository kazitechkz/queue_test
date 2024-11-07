from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile, File, Form, Path

from app.core.auth_core import check_employee, check_client
from app.feature.order.dtos.order_dto import OrderRDTO
from app.feature.order.filter.order_filter import OrderFiltersForPaymentDocuments
from app.feature.order.order_repository import OrderRepository
from app.feature.payment_document.dtos.payment_document_dto import PaymentDocumentRDTO
from app.feature.payment_document.payment_document_repository import PaymentDocumentRepository
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class PaymentDocumentController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.post(
            "/upload-payment-file",
            summary="Прикрепление документов для проверки"
        )(self.upload_payment_doc)
        self.router.post(
            "/get-payment-docs",
            summary="Получение всех документов"
        )(self.get_payment_docs)
        self.router.get(
            "/get-payment-doc-by-order-id/{order_id}",
            summary="Получение документов по номеру заказа"
        )(self.get_payment_doc_by_order)
        self.router.post(
            "/add-comment-to-doc",
            response_model=PaymentDocumentRDTO,
            summary="Подтверждение или отклонение документа"
        )(self.add_to_comment_to_doc)
        self.router.post(
            "/make-decision",
            response_model=OrderRDTO,
            summary="Принятие или отклонение решения"
        )(self.make_decision)

    async def upload_payment_doc(
            self,
            documents: List[UploadFile] = File(..., description="Файл для загрузки"),
            order_id: int = Form(..., description="Идентификатор заказа"),
            repo: PaymentDocumentRepository = Depends(PaymentDocumentRepository),
            orderRepo: OrderRepository = Depends(OrderRepository),
            userRepo: UserRDTOWithRelations = Depends(check_client)
    ):
        results = []
        for document in documents:
            result = await repo.upload_file(userRepo=userRepo, order_id=order_id, file=document, orderRepo=orderRepo)
            results.append(result)
        await repo.update_order(orderRepo=orderRepo, order_id=order_id)
        return {"message": "Файлы успешно загружены", "results": results}

    async def get_payment_docs(self,
                               params: OrderFiltersForPaymentDocuments = Depends(),
                               repo: PaymentDocumentRepository = Depends(PaymentDocumentRepository),
                               orderRepo: OrderRepository = Depends(OrderRepository),
                               userRepo: UserRDTOWithRelations = Depends(check_employee)
                               ):
        return await repo.get_payment_docs(orderRepo=orderRepo, params=params, userRepo=userRepo)

    async def get_payment_doc_by_order(self,
                                       order_id: int = Path(..., description="Идентификатор заказа"),
                                       repo: PaymentDocumentRepository = Depends(PaymentDocumentRepository),
                                       orderRepo: OrderRepository = Depends(OrderRepository)
                                       ):
        return await repo.get_payment_doc_by_order(orderRepo=orderRepo, order_id=order_id)

    async def add_to_comment_to_doc(self,
                                    payment_id: int = Form(..., description="Идентификатор документа"),
                                    status: bool = Form(..., description="Статус документа"),
                                    comment: Optional[str] = Form(None, description="Комментарии к документу"),
                                    repo: PaymentDocumentRepository = Depends(PaymentDocumentRepository),
                                    userRepo: UserRDTOWithRelations = Depends(check_employee)
                                    ):
        return await repo.add_comment_to_doc(payment_id=payment_id, status=status, comment=comment, userRepo=userRepo)

    async def make_decision(self,
                            repo: PaymentDocumentRepository = Depends(PaymentDocumentRepository),
                            orderRepo: OrderRepository = Depends(OrderRepository),
                            payment_id: int = Form(..., description="Идентификатор документа"),
                            status: bool = Form(..., description="Статус документа"),
                            userRepo: UserRDTOWithRelations = Depends(check_employee)
                            ):
        return await repo.make_decision(payment_id=payment_id, orderRepo=orderRepo, status=status, userRepo=userRepo)
