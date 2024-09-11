from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.material_model import MaterialModel


class MaterialRepository(BaseRepository[MaterialModel]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(MaterialModel, db)