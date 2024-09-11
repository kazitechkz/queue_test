from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.core.database import init_db
from app.feature.organization.organization_controller import OrganizationController
from app.feature.organization_employee.organization_employee_controller import OrganizationEmployeeController
from app.feature.organization_type.organization_type_controller import OrganizationTypeController
from app.feature.region.region_controller import RegionController
from app.feature.role.role_controller import RoleController
from app.feature.user.user_controller import UserController
from app.feature.user_type.user_type_controller import UserTypeController
from app.feature.vehicle_category.vehicle_category_controller import VehicleCategoryController
from app.feature.vehicle_color.vehicle_color_controller import VehicleColorController


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
vehicle_color = VehicleColorController()
vehicle_category = VehicleCategoryController()
region = RegionController()

app.include_router(role_controller.router, prefix="/role", tags=["role"])
app.include_router(user_type_controller.router, prefix="/user-type", tags=["user-type"])
app.include_router(user_controller.router, prefix="/user", tags=["user"])
app.include_router(organization_type_controller.router, prefix="/organization-type", tags=["organization-type"])
app.include_router(organization_controller.router, prefix="/organization", tags=["organization"])
app.include_router(organization_employee_controller.router, prefix="/organization-employee", tags=["organization-employee"])
app.include_router(vehicle_color.router, prefix="/vehicle-color", tags=["vehicle-color"])
app.include_router(vehicle_category.router, prefix="/vehicle-category", tags=["vehicle-category"])
app.include_router(region.router, prefix="/region", tags=["region"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000,reload=True)