from typing import Iterable
import uuid

from ..models.models import Vehicle
from ..models.adminstration import User, Role
from ..models.requests_responses import (
    GetVehicleLocationReq,
    VehicleLocation,
    SetVehicleLocationReq,
    VehicleLocationChangedRes,
)

from ..data_access.sqlit_repos import vehicle_repo as vhl_repo, driver_repo
from .administration import PrivilageError

def _filter_vehicles_by_office(vehicles: Iterable[Vehicle], office_id: uuid.UUID) -> Iterable[Vehicle]:
    for v in vehicles:
        if v.office_id == office_id:
            yield v



def get_office_vehicles(user: User, office_id: uuid.UUID):
    return _filter_vehicles_by_office(vhl_repo.get_all(), office_id)


def get_all_vehicles(user: User) -> Iterable[Vehicle]:
    if user.role != Role.ROOT:
        raise PrivilageError()
    return vhl_repo.get_all()


def get_vehicle_location(req: GetVehicleLocationReq) -> VehicleLocation:
    # v = vhl_repo.get(req.id)
    # return v.current_location
    ...

def set_vehicle_location(req: SetVehicleLocationReq) -> VehicleLocationChangedRes:
    # v = vhl_repo.get(req.vehicle_id)
    # v.set_location(req.location)
    ...