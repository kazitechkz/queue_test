from abc import ABC, abstractmethod

from fastapi import Query


class BaseFilter(ABC):
    def __init__(
        self,
        per_page: int = Query(
            default=20, gt=0, example=20, description="Количество элементов на страницу"
        ),
        page: int = Query(default=1, ge=1, example=1, description="Номер страницы"),
        search: str | None = Query(
            default=None, max_length=255, min_length=3, description="Поисковый запрос"
        ),
    ) -> None:
        self.per_page = per_page
        self.page = page
        self.search = search

    @abstractmethod
    def apply(self) -> list:
        pass
