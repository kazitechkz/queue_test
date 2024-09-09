from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.core.database import init_db
from app.feature.organization_type.organization_type_controller import OrganizationTypeController
from app.feature.role.role_controller import RoleController
from app.feature.user.user_controller import UserController
from app.feature.user_type.user_type_controller import UserTypeController


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
        title="DIGITAL QUEUE TEST",
        description="Электронно-цифровая очередь",
        version="0.1",
        lifespan=lifespan
    )

role_controller = RoleController()
user_type_controller = UserTypeController()
user_controller = UserController()
organization_type_controller = OrganizationTypeController()

app.include_router(role_controller.router, prefix="/role", tags=["role"])
app.include_router(user_type_controller.router, prefix="/user-type", tags=["user-type"])
app.include_router(user_controller.router, prefix="/user", tags=["user"])
app.include_router(organization_type_controller.router, prefix="/organization-type", tags=["organization-type"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000,reload=True)