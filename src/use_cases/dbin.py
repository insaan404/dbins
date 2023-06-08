import uuid
from typing import Iterable

from ..models.models import DustBin
from ..models.adminstration import User, Role
from ..models.requests_responses import (
    InstallDBinReq,
)

from src.events.event_store import EventStore

from ..data_access.sqlit_repos import dbin_repo, driver_repo
from .administration import PrivilageError


event_store = EventStore()


def _get_dbin_by_identifier(dbins: Iterable[DustBin], identifier: str) -> DustBin:
    for dbin in dbins:
        if dbin.identifier == identifier:
            return dbin


def _filter_dbins_by_office(dbins: Iterable[DustBin], office_id) -> Iterable[DustBin]:
    for dbin in dbins:
        if dbin.office_id == office_id:
            yield dbin


def get_office_dbins(user: User, office_id: uuid.UUID) -> Iterable[DustBin]:
    driver = driver_repo.get(user.driver_id)
    if user.role == Role.DRIVER and driver.office_id != office_id:
        PrivilageError()

    return _filter_dbins_by_office(dbin_repo.get_all(), office_id)



def install_dustbin(user: User, req: InstallDBinReq) -> DustBin:
    if user.role != Role.ROOT:
        raise PrivilageError()

    dbin = DustBin(uuid.uuid4(), req.name, req.identifier, req.location, req.depth, req.office_id)
    dbin_repo.add(dbin)
    return dbin


def change_dbin_level(identifier: str, level: float) -> bool:
    # breakpoint()
    dbin = _get_dbin_by_identifier(dbin_repo.get_all(), identifier)
    dbin.set_level(level)
    if dbin.level_status > 80:
        event_store.dbin_filled({"id": str(dbin.id), "level_status": dbin.level_status})
    else:
        event_store.dbin_emptied({"id": str(dbin.id), "level_status": dbin.level_status})
    return True


def get_dustbin(user: User, id: uuid.UUID) -> DustBin:
    dbin = dbin_repo.get(id)

    driver = driver_repo.get(user.driver_id)
    if user.role == Role.DRIVER and driver.office_id != dbin.office_id:
        raise PrivilageError()
    return dbin


def get_all_dustbins(user: User) -> Iterable[DustBin]:
    if user.role != Role.ROOT:
        raise PrivilageError()
    return dbin_repo.get_all()







