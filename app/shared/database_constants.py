from datetime import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import mapped_column

ID = Annotated[int, mapped_column(primary_key=True)]
CreatedAt = Annotated[datetime, mapped_column(server_default=text("CURRENT_TIMESTAMP"))]
UpdatedAt = Annotated[datetime, mapped_column(server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.now())]


class AppTableNames():
    RoleTableName = "roles"
    UserTypeTableName = "user_types"
    UserTableName = "users"
    OrganizationTypeTableName = "organization_types"
    OrganizationTableName = "organizations"
    OrganizationEmployeeTableName = "organization_employees"
    VehicleColorTableName = "vehicle_colors"
    VehicleCategoryTableName = "vehicle_categories"
    RegionTableName = "regions"


class TableConstantsNames:
    UserLegalTypeId = 2
    UserLegalTypeValue = "legal_entity"

