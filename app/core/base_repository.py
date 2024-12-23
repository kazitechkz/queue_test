from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import and_, asc, desc, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.app_exception_response import AppExceptionResponse
from app.core.database import get_db
from app.core.pagination_dto import Pagination


# Определение типа модели
T = TypeVar("T")


class BaseRepository(Generic[T]):
    _instance = None

    def __init__(self, model: type[T], db: Session) -> None:
        self.model = model
        self.db = db

    async def get_all_with_filter(self, filters: list = [], options: list = []):
        # Создаем запрос
        query = select(self.model)

        # Применяем опции (например, связанные данные)
        if options:
            for option in options:
                query = query.options(option)

        # Применяем фильтры
        for filter_condition in filters:
            query = query.filter(filter_condition)

        # Выполняем запрос
        results = await self.db.execute(query)

        # Получаем все записи
        items = results.scalars().all()

        return items

    async def get_first_with_filter(self, filters: list = [], options: list = []):
        query = select(self.model)
        if options:
            for option in options:
                query = query.options(option)
        # Применение фильтров к запросу
        for filter_condition in filters:
            query = query.filter(filter_condition)
        results = await self.db.execute(query)
        item = results.scalars().first()
        return item

    async def paginate_with_filter(
        self,
        dto: BaseModel,
        page: int = 1,
        per_page: int = 20,
        filters: list = [],
        options: list = [],
    ):
        query = select(self.model)
        if options:
            query = query.options(*options)
        # Применение фильтров к запросу
        for filter_condition in filters:
            query = query.filter(filter_condition)
        # Подсчет общего количества элементов
        count_query = select(func.count()).select_from(query.subquery())
        total_items = await self.db.scalar(count_query)
        total_pages = (total_items + per_page - 1) // per_page
        # Получение элементов для текущей страницы
        results = await self.db.execute(
            query.limit(per_page).offset((page - 1) * per_page)
        )
        items = results.scalars().all()

        dto_items = [dto.from_orm(item) for item in items]

        result = Pagination(
            items=dto_items,
            per_page=per_page,
            page=page,
            total_pages=total_pages,
            total_items=total_items,
        )
        return result

    async def get(self, id: int, options: list | None = None):
        query = select(self.model)
        if options is not None:
            for option in options:
                query = query.options(option)
        query = query.filter(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_filtered(self, filters: dict[str, Any], options: list | None = None):
        query = select(self.model)
        if options:
            for option in options:
                query = query.options(option)

        if filters:
            for key, value in filters.items():
                column = getattr(self.model, key, None)
                if column is not None:
                    query = query.filter(column == value)

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_with_filter(self, filters: [], options: list | None = None):
        query = select(self.model)
        if options:
            for option in options:
                query = query.options(option)
        # Применение фильтров к запросу
        for filter_condition in filters:
            query = query.filter(filter_condition)

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_first_with_filters(
        self,
        filters: list = [],
        options: list | None = None,
        order_by: list | None = None,
    ):
        query = select(self.model)
        if options:
            for option in options:
                query = query.options(option)

        if filters:
            conditions = []
            for filter_condition in filters:
                for key, value in filter_condition.items():
                    # Dynamically create the filter condition using getattr
                    conditions.append(getattr(self.model, key) == value)

            # Apply the filter conditions to the query
            if conditions:
                query = query.filter(and_(*conditions))

        # Apply ordering if the order_by parameter is provided
        if order_by:
            order_clauses = []
            for field in order_by:
                if isinstance(field, str):
                    # Default to ascending if only field name is provided
                    order_clauses.append(asc(getattr(self.model, field)))
                elif isinstance(field, tuple) and len(field) == 2:
                    # Allow specifying order as ("field_name", "asc" or "desc")
                    field_name, direction = field
                    if direction == "desc":
                        order_clauses.append(desc(getattr(self.model, field_name)))
                    else:
                        order_clauses.append(asc(getattr(self.model, field_name)))
            query = query.order_by(*order_clauses)

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all(self) -> list[T]:
        result = await self.db.execute(select(self.model))
        return result.scalars().all()

    async def create(self, obj: T) -> T:
        try:
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
        except IntegrityError as e:
            await self.db.rollback()
            await self.refresh_db()
            raise ValueError(self._parse_integrity_error(e))

    async def create_all(self, obj: [T]):
        try:
            self.db.add_all(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
        except IntegrityError as e:
            await self.db.rollback()
            await self.refresh_db()
            raise ValueError(self._parse_integrity_error(e))

    async def update(self, obj: T, dto: BaseModel) -> T:
        try:
            for field, value in dto.dict(exclude_unset=True).items():
                setattr(obj, field, value)
            await self.db.commit()
            return obj
        except IntegrityError as e:
            await self.db.rollback()
            await self.refresh_db()
            raise ValueError(self._parse_integrity_error(e))

    async def filter_and_update(
        self, update_values: dict[str, Any], filters: list[dict[str, Any]] = []
    ):
        # Step 1: Filter rows
        query = select(self.model)
        if filters:
            conditions = []
            for filter_condition in filters:
                for key, value in filter_condition.items():
                    # Dynamically create filter condition using getattr
                    conditions.append(getattr(self.model, key) == value)

            # Apply combined conditions to the query
            if conditions:
                query = query.filter(and_(*conditions))

        # Execute the query to get filtered rows
        results = await self.db.execute(query)
        filtered_items = results.scalars().all()

        # Step 2: Update filtered rows
        if filtered_items:
            # Prepare update statement with the gathered filter
            stmt = update(self.model).values(**update_values).where(and_(*conditions))

            # Execute the update statement
            result = await self.db.execute(stmt)
            await self.db.commit()  # Commit the transaction

            return result.rowcount  # Return the number of rows affected

        return 0

    async def update_with_filters(
        self, update_values: dict[str, Any], filters: list = []
    ):
        stmt = update(self.model).values(**update_values).where(*filters)
        result = await self.db.execute(stmt)
        await self.db.commit()  # Commit the transaction
        return result.rowcount  # Return the number of rows affected

    async def delete(self, id: int) -> None:
        result = await self.get(id)
        if result is None:
            raise AppExceptionResponse.not_found(message="Не найдено")
        await self.db.delete(result)
        await self.db.commit()

    async def refresh_db(self) -> None:
        self.db = await anext(get_db())

    def _parse_integrity_error(self, error: IntegrityError) -> str:
        orig_msg = str(error.orig)
        err_msg = orig_msg.split(":")[-1].replace("\n", "").strip()

        parts = err_msg.split(".")
        if len(parts) >= 2:
            table, column = parts[-2], parts[-1]
            return f"Duplicate entry for {column} in {table}. Please choose a different value."
        return "An error occurred while processing your request."
