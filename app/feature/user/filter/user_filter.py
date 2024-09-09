from typing import Optional
from fastapi import Query
from sqlalchemy import or_, and_

from app.core.base_filter import BaseFilter
from app.domain.models.user_model import UserModel


class UserFilter(BaseFilter):
    def __init__(self,
                 per_page: int = Query(default=20, gt=0, example=20, description="Количество элементов на страницу"),
                 page: int = Query(default=1, ge=1, example=1, description="Номер страницы"),
                 search: Optional[str] = Query(default=None, max_length=255, min_length=3,
                                               description="Поисковый запрос по имени, телефону, почте, иину"),
                 role_id: Optional[int] = Query(default=None, gt=0, description="Введите роль пользователя"),
                 type_id: Optional[int] = Query(default=None, gt=0, description="Введите тип пользователя")):
        super().__init__(per_page, page, search)
        self.per_page = per_page
        self.page = page
        self.search = search
        self.role_id = role_id
        self.type_id = type_id
        self.model = UserModel

    def apply(self) -> list:
        filters = []
        if (self.search):
            filters.append(or_(
                self.model.email.like(f"%{self.search}%"),
                self.model.phone.like(f"%{self.search}%"),
                self.model.iin.like(f"%{self.search}%"),
                self.model.name.like(f"%{self.search}%"),
                )
            )
        if (self.role_id):
            filters.append(and_(self.model.role_id == self.role_id))
        if (self.type_id):
            filters.append(and_(self.model.type_id == self.type_id))
        return filters
