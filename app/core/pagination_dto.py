# Generic тип для модели данных
from typing import List, Generic, TypeVar

from pydantic import BaseModel
from pydantic.v1.generics import GenericModel

T = TypeVar('T')


class Pagination(Generic[T]):
    current_page: int
    last_page: int
    total_pages: int
    total_items: int
    items: List[T]

    def __init__(self, items: List[T], total_pages: int, total_items: int, per_page: int, page: int):
        self.items = items
        self.total_pages = total_pages
        self.total_items = total_items
        self.current_page = page
        self.last_page = (total_pages + per_page - 1) // per_page

