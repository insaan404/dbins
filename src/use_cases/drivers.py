import uuid
from typing import Iterable

from src.data_access.sql_models import Driver
from ..models.models import Driver
from ..models.adminstration import User, Role
from .administration import PrivilageError
from ..data_access.sqlit_repos import driver_repo as repo

from ..models.requests_responses import (AddDriverToOfficeReq, MakeEmployDriverForOffice, AssignVehicleToDriver)




def _filter_office_drivers(drivers: Iterable[Driver], office_id: uuid.UUID) -> Iterable[Driver]:
    for driver in drivers:
        if driver.office_id == office_id:
            yield driver



def all_drivers(user: User) -> Iterable[Driver]:
    if user.role != Role.ROOT:
        raise PrivilageError()
    return repo.get_all()



def get_driver(user: User, id: uuid.UUID) -> Driver:
    if user.role == Role.DRIVER and user.driver_id != id:
        raise PrivilageError()
    
    return repo.get(id)


def get_office_drivers(user: User, office_id: uuid.UUID):
    if user.role == Role.DRIVER:
        raise PrivilageError()
    return _filter_office_drivers(repo.get_all(), office_id)


def create_and_add_driver_to_office(user: User, req: AddDriverToOfficeReq) -> Driver:
    if user.role != Role.ROOT:
        raise PrivilageError()
    
    driver = Driver(uuid.uuid4(), req.fname, req.lname, req.address, req.contact, req.office_id, req.vehicle_id)
    repo.add(driver)
    return driver


def make_employ_driver_for_office(user: User, req: MakeEmployDriverForOffice) -> Driver:
    ...


def assign_vehicle_to_employ(user: User, req: AssignVehicleToDriver) -> Driver:
    ...