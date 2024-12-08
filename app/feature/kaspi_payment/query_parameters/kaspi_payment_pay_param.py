from fastapi import Query


class KaspiPaymentPayParam:
    def __init__(
        self,
        command: str = Query(max_length=255, description="Команда от Kaspi"),
        txn_id: str = Query(
            max_length=20, description="Уникальный идентификатор KASPI платежа"
        ),
        txn_date: str = Query(
            max_length=50, description="ГГГГММДДЧЧММСС", examples="20240917100102"
        ),
        account: str = Query(max_length=20, description="Номер заказа для kaspi"),
        sum: str | None = Query(
            default=None,
            description="Сумма к зачислению в формате '500.00'",
            example="500.00",
        ),
    ) -> None:
        self.command = command
        self.txn_id = txn_id
        self.txn_date = txn_date
        self.account = account
        self.sum = sum
