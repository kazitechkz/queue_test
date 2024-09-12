from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.core.database import init_db
from app.feature.factory.factory_controller import FactoryController
from app.feature.material.material_controller import MaterialController
from app.feature.organization.organization_controller import OrganizationController
from app.feature.organization_employee.organization_employee_controller import OrganizationEmployeeController
from app.feature.organization_type.organization_type_controller import OrganizationTypeController
from app.feature.region.region_controller import RegionController
from app.feature.role.role_controller import RoleController
from app.feature.user.user_controller import UserController
from app.feature.user_type.user_type_controller import UserTypeController
from app.feature.vehicle.vehicle_controller import VehicleController
from app.feature.vehicle_category.vehicle_category_controller import VehicleCategoryController
from app.feature.vehicle_color.vehicle_color_controller import VehicleColorController
from app.feature.workshop.workshop_controller import WorkshopController


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
        title="DIGITAL QUEUE TEST",
        description="Электронно-цифровая очередь",
        version="0.1",
        lifespan=lifespan,
        debug=True
    )

role_controller = RoleController()
user_type_controller = UserTypeController()
user_controller = UserController()
organization_type_controller = OrganizationTypeController()
organization_controller = OrganizationController()
organization_employee_controller = OrganizationEmployeeController()
vehicle_color_controller = VehicleColorController()
vehicle_category_controller = VehicleCategoryController()
region_controller = RegionController()
vehicle_controller = VehicleController()
factory_controller = FactoryController()
workshop_controller = WorkshopController()
material_controller = MaterialController()

app.include_router(role_controller.router, prefix="/role", tags=["role"])
app.include_router(user_type_controller.router, prefix="/user-type", tags=["user-type"])
app.include_router(user_controller.router, prefix="/user", tags=["user"])
app.include_router(organization_type_controller.router, prefix="/organization-type", tags=["organization-type"])
app.include_router(organization_controller.router, prefix="/organization", tags=["organization"])
app.include_router(organization_employee_controller.router, prefix="/organization-employee", tags=["organization-employee"])
app.include_router(vehicle_color_controller.router, prefix="/vehicle-color", tags=["vehicle-color"])
app.include_router(vehicle_category_controller.router, prefix="/vehicle-category", tags=["vehicle-category"])
app.include_router(region_controller.router, prefix="/region", tags=["region"])
app.include_router(vehicle_controller.router, prefix="/vehicle", tags=["vehicle"])
app.include_router(factory_controller.router, prefix="/factory", tags=["factory"])
app.include_router(workshop_controller.router, prefix="/workshop", tags=["workshop"])
app.include_router(material_controller.router, prefix="/material", tags=["material"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000,reload=True)