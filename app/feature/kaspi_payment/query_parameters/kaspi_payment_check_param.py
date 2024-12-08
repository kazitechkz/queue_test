from fastapi import Query


class KaspiPaymentCheckParam:
    def __init__(
        self,
        command: str = Query(max_length=255, description="Команда от Kaspi"),
        txn_id: str = Query(
            max_length=20, description="Уникальный идентификатор KASPI платежа"
        ),
        account: str = Query(max_length=20, description="Номер заказа для kaspi"),
        sum: str | None = Query(
            default=None, description="Sum in format '200.00'", example="200.00"
        ),
    ) -> None:
        self.command = command
        self.txn_id = txn_id
        self.account = account
        self.sum = sum
