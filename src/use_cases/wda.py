import uuid
from typing import Iterable

from src.data_access.sqlit_repos import office_repo
from ..models.adminstration import User, Role
from ..models.requests_responses import AddWDAReq
from .administration import PrivilageError
from ..models.models import WastDisposalArea
from ..data_access.sqlit_repos import wda_repo 
from ..data_access.sqlit_repos import driver_repo
from ..data_access.sqlit_repos import office_repo



def get_office_wda(user: User, id: uuid.UUID) -> WastDisposalArea:
    if user.role == Role.ROOT:
        return wda_repo.get(id)
    driver = driver_repo.get(user.driver_id)
    if driver.office_id != id:
        raise PrivilageError()
    
    office = office_repo.get(id)
    return wda_repo.get(office.wda_id)


def add_wda(user: User, req: AddWDAReq) -> WastDisposalArea:
    if user.role != Role.ROOT:
        raise PrivilageError()

    wda = WastDisposalArea(uuid.uuid4(), req.name, req.location, req.area)
    wda_repo.add(wda)
    return wda

    

def get_wda(user: User, id: uuid.UUID) -> WastDisposalArea:
    return wda_repo.get(id)


def get_all(user: User):
    if user.role == Role.DRIVER:
        raise PrivilageError()
    return wda_repo.get_all()












