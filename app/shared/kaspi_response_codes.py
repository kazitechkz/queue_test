from sqlalchemy import Enum


class KaspiPaymentStatus(Enum):
    AVAILABLE_FOR_PAYMENT = (
        0  # абонент/счёт/заказ найден и доступен для пополнения/оплаты
    )
    NOT_FOUND = 1  # "абонент/счёт не найден" или "заказ не найден", если запрос check был на проверку состояния заказа
    CANCELLED = 2  # заказ отменен
    ALREADY_PAID = 3  # заказ уже оплачен
    PAYMENT_IN_PROCESS = 4  # платеж в обработке
    PROVIDER_ERROR = 5  # Другие ответы


class KaspiPaymentCodeStatus:
    CHECK: str = "check"
    PAY: str = "pay"
