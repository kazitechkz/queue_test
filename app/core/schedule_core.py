from app.domain.models.vehicle_model import VehicleModel


def get_vehicle_information(vehicle: VehicleModel) -> str:
    return f"{vehicle.registration_number} - {vehicle.car_model}"
