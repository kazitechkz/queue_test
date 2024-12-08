from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.app_exception_response import AppExceptionResponse
from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.material_model import MaterialModel


class MaterialRepository(BaseRepository[MaterialModel]):
    def __init__(self, db: Session = Depends(get_db)) -> None:
        super().__init__(MaterialModel, db)

    async def count_price(self, sap_id: str, quan: int) -> dict | None:
        material = await self.get_filtered(filters={"sap_id": sap_id})
        if material is None:
            raise AppExceptionResponse.bad_request(message="Материал не найден")
        return {
            "price_without_taxes": material.price_without_taxes * quan,
            "price_with_taxes": material.price_with_taxes * quan,
            "material": material,
        }
