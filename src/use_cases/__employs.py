import uuid
from typing import Iterable

from ..models.models import Employ
# from ..data_access.repos import EmployRepository
from ..data_access.sqlit_repos import emp_repo as repo
from ..models.adminstration import User, Role
from .administration import PrivilageError



# repo = EmployRepository()


def _employs_by_office_id(employs: Iterable[Employ], office_id: uuid.UUID):
    for emp in employs:
        if emp.office_id == office_id:
            yield emp


def get_employ(user: User, emp_id: uuid.UUID) -> Employ:
    if user.role == Role.USER and user.employ_id != emp_id:
        raise PrivilageError()
    
    emp = repo.get(emp_id)
    if user.role == Role.ADMIN:
        user_emp = repo.get(user.employ_id)
        if emp.office_id != user_emp.office_id:
            raise PrivilageError()
        return emp
    
    return emp
        

def get_office_employs(user: User, office_id: uuid.UUID) -> Iterable[Employ]:
    if user.role == Role.USER:
        raise PrivilageError()
    elif user.role == Role.ADMIN:
        admin = repo.get(user.employ_id)
        if admin.office_id == office_id:
            return _employs_by_office_id(repo.get_all(), office_id)
        else:
            raise PrivilageError()
    
    return _employs_by_office_id(repo.get_all(), office_id)


def get_all(user: User) -> Iterable[Employ]:
    if user.role != Role.ROOT:
        raise PrivilageError()
    
    return repo.get_all()
