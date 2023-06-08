import uuid
from typing import Iterable
from ..models.models import Office
from ..models.adminstration import User, Role
from .administration import PrivilageError


from ..data_access.sqlit_repos import office_repo as repo



def get_all_offices(user: User) -> Iterable[Office]:
    if user.role != Role.ROOT:
        raise PrivilageError()
    offices = repo.get_all()
    return offices


def get_by_id(user: User, id: uuid.UUID) -> Office:
    if not (user.role == Role.ROOT or user.role == Role.ADMIN):
        raise PrivilageError()
    return repo.get(id)


def get_by_name(user: User, area_name: str) -> Office:
    if not (user.role == Role.ROOT or user.role == Role.ADMIN):
        raise PrivilageError()
    
    # offices = repo.get_all()

    # for o in offices:
    #     if o.area_name == area_name:
    #         return o
        
