from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.order_status_model import OrderStatusModel


class OrderStatusRepository(BaseRepository[OrderStatusModel]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(OrderStatusModel, db)