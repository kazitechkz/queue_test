from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Depends
from app.core.database import init_db, get_db
from app.core.seed_database import seed_database
from app.feature.auth.auth_controller import AuthController
from app.feature.factory.factory_controller import FactoryController
from app.feature.kaspi_payment.kaspi_payment_controller import KaspiPaymentController
from app.feature.material.material_controller import MaterialController
from app.feature.operation.operation_controller import OperationController
from app.feature.order.order_controller import OrderController
from app.feature.organization.organization_controller import OrganizationController
from app.feature.organization_employee.organization_employee_controller import OrganizationEmployeeController
from app.feature.organization_type.organization_type_controller import OrganizationTypeController
from app.feature.region.region_controller import RegionController
from app.feature.role.role_controller import RoleController
from app.feature.sap_request.sap_request_controller import SapRequestController
from app.feature.schedule.schedule_controller import ScheduleController
from app.feature.schedule_history.schedule_history_controller import ScheduleHistoryController
from app.feature.test.test_controller import TestController
from app.feature.user.user_controller import UserController
from app.feature.user_type.user_type_controller import UserTypeController
from app.feature.vehicle.vehicle_controller import VehicleController
from app.feature.vehicle_category.vehicle_category_controller import VehicleCategoryController
from app.feature.vehicle_color.vehicle_color_controller import VehicleColorController
from app.feature.workshop.workshop_controller import WorkshopController
from app.feature.workshop_schedule.workshop_schedule_controller import WorkshopScheduleController


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
auth_controller = AuthController()
order_controller = OrderController()
sap_request_controller = SapRequestController()
kaspi_payment_controller = KaspiPaymentController()
operation_controller = OperationController()
workshop_schedule_controller = WorkshopScheduleController()
schedule_controller = ScheduleController()
schedule_history_controller = ScheduleHistoryController()
test_controller = TestController()

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
app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
app.include_router(order_controller.router, prefix="/order", tags=["order"])
app.include_router(sap_request_controller.router, prefix="/sap-request", tags=["sap-request"])
app.include_router(kaspi_payment_controller.router, prefix="/kaspi", tags=["kaspi"])
app.include_router(operation_controller.router, prefix="/operation", tags=["operation"])
app.include_router(workshop_schedule_controller.router, prefix="/workshop-schedule", tags=["workshop-schedule"])
app.include_router(schedule_controller.router, prefix="/schedule", tags=["schedule"])
app.include_router(schedule_history_controller.router, prefix="/schedule-history", tags=["schedule-history"])
app.include_router(test_controller.router, prefix="/test", tags=["test"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000,reload=True)