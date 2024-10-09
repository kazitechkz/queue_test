from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import selectinload

from app.feature.act_weight.act_weight_repository import ActWeightRepository
from app.feature.act_weight.dtos.act_weight_dto import ActWeightRelationsDTO
from app.feature.act_weight.filter.ActWeightFilter import ActWeightFilter


class ActWeightController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/all")(self.all)
        self.router.get("/get/{id}", response_model=ActWeightRelationsDTO)(self.get)

    #Only for admin and employee
    async def all(self,
                  params:ActWeightFilter = Depends(ActWeightFilter),
                  repo: ActWeightRepository = Depends(ActWeightRepository),

                  ):
        result = await repo.paginate_with_filter(
            dto=ActWeightRelationsDTO,
            page=params.page,
            per_page=params.per_page,
            filters=params.apply(),
            options=[
                selectinload(repo.model.history),
                selectinload(repo.model.responsible),
                selectinload(repo.model.order),
                selectinload(repo.model.vehicle),
                selectinload(repo.model.trailer),
            ]
        )
        return result

    async def get(self,
                  id:int = Path(gt=0,description="Идентификатор акта взвешивания"),
                  repo: ActWeightRepository = Depends(ActWeightRepository),
                  )->ActWeightRelationsDTO:
        result = await repo.get(
            id=id,
            options=[
                selectinload(repo.model.history),
                selectinload(repo.model.responsible),
                selectinload(repo.model.order),
                selectinload(repo.model.vehicle),
                selectinload(repo.model.trailer),
            ]
        )
        result_dto = ActWeightRelationsDTO.from_orm(result)
        return result_dto