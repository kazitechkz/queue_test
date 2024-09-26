from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.kaspi_payment_model import KaspiPaymentModel
from app.feature.kaspi_payment.dtos.kaspi_payment_dto import KaspiPaymentCheckResponseDTO, KaspiPaymentCDTO, \
    KaspiPaymentPayResponseDTO
from app.feature.kaspi_payment.query_parameters.kaspi_payment_check_param import KaspiPaymentCheckParam
from app.feature.kaspi_payment.query_parameters.kaspi_payment_pay_param import KaspiPaymentPayParam
from app.feature.order.dtos.order_dto import OrderCDTO
from app.feature.order.order_repository import OrderRepository
from app.shared.kaspi_response_codes import KaspiPaymentStatus, KaspiPaymentCodeStatus


class KaspiPaymentRepository(BaseRepository[KaspiPaymentModel]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(KaspiPaymentModel, db)

    async def check(
            self,
            kaspiParams: KaspiPaymentCheckParam,
            orderRepo: OrderRepository
    ):
        try:
            order = await orderRepo.get_first_with_filters(filters=[{"zakaz": kaspiParams.account}])
            if order is None:
                return KaspiPaymentCheckResponseDTO(txn_id=kaspiParams.txn_id, sum=0,
                                                    result=KaspiPaymentStatus.NOT_FOUND, comment="Заказ не найден")
            if order.is_paid and order.txn_id:
                return KaspiPaymentCheckResponseDTO(txn_id=kaspiParams.txn_id, sum=order.price_with_taxes,
                                                    result=KaspiPaymentStatus.ALREADY_PAID,
                                                    comment="Заказ уже оплачен")

            update_values = {"is_failed": True}  # Fields to update
            filters = [{"account": kaspiParams.account}, {"command": KaspiPaymentCodeStatus.CHECK},
                       {"is_failed": False}]
            prev_kaspi_payments = await self.filter_and_update(filters=filters, update_values=update_values)

            kaspi_payment_dto = (
                KaspiPaymentCDTO(
                    order_id=order.id,
                    zakaz=kaspiParams.account,
                    account=kaspiParams.account,
                    txn_id=kaspiParams.txn_id,
                    txn_check_id=kaspiParams.txn_id,
                    command=KaspiPaymentCodeStatus.CHECK,
                    sum=order.price_with_taxes,
                    amount=order.quan
                ))
            kaspi_payment = await  self.create(KaspiPaymentModel(**kaspi_payment_dto.dict()))
            return KaspiPaymentCheckResponseDTO(txn_id=kaspi_payment.txn_id, sum=kaspi_payment.sum,
                                                result=KaspiPaymentStatus.AVAILABLE_FOR_PAYMENT,
                                                comment="Заказ готов к оплате")

        except:
            return KaspiPaymentCheckResponseDTO(txn_id=kaspiParams.txn_id, sum=kaspiParams.sum,
                                                result=KaspiPaymentStatus.PROVIDER_ERROR,
                                                comment="Ошибка")

    async def pay(
            self,
            kaspiParams: KaspiPaymentPayParam,
            orderRepo: OrderRepository,

    ):

        order = await orderRepo.get_first_with_filters(filters=[{"zakaz": kaspiParams.account}])
        if order is None:
            return KaspiPaymentPayResponseDTO(
                txn_id=kaspiParams.txn_id, sum=0,
                result=KaspiPaymentStatus.NOT_FOUND,
                prv_txn_id=kaspiParams.account,
                comment="Заказ не найден")
        if order.is_paid and order.txn_id:
            return KaspiPaymentPayResponseDTO(txn_id=kaspiParams.txn_id, sum=order.price_with_taxes,
                                              prv_txn_id=kaspiParams.account,
                                              result=KaspiPaymentStatus.ALREADY_PAID,
                                              comment="Заказ уже оплачен")

        check_payment = await self.get_first_with_filters(
            filters=[{"is_failed": False}, {"account": kaspiParams.account}, {"command": KaspiPaymentCodeStatus.CHECK}])
        if not check_payment:
            return KaspiPaymentPayResponseDTO(txn_id=kaspiParams.txn_id, sum=0, result=KaspiPaymentStatus.NOT_FOUND,
                                              prv_txn_id=kaspiParams.account,
                                              comment="Заказ не найден")

        check_payment_dto = KaspiPaymentCDTO.from_orm(check_payment)
        check_payment_dto.txn_pay_id = kaspiParams.txn_id
        check_payment_dto.txn_id = kaspiParams.txn_id
        check_payment_dto.txn_date = kaspiParams.txn_date
        check_payment_dto.command = KaspiPaymentCodeStatus.PAY
        check_payment_dto.is_paid = True
        check_payment_dto.paid_at = datetime.strptime(kaspiParams.txn_date, "%Y%m%d%H%M%S")
        paid_payment = await self.update(obj=check_payment, dto=check_payment_dto)
        order_dto = OrderCDTO.from_orm(order)
        order_dto.kaspi_id = paid_payment.id
        order_dto.txn_id = paid_payment.txn_id
        order_dto.is_paid = True
        order_dto.status_id = 5
        order_dto.paid_at = paid_payment.paid_at
        paid_order = await orderRepo.update(obj=order, dto=order_dto)
        return KaspiPaymentPayResponseDTO(txn_id=paid_order.txn_id, sum=0,
                                          result=KaspiPaymentStatus.AVAILABLE_FOR_PAYMENT,
                                          prv_txn_id=kaspiParams.account,
                                          comment="Заказ оплачен")
