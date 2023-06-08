from typing import Iterable, Optional
import uuid
from dataclasses import dataclass

from .models import Driver, Vehicle, DustBin, Office, WastDisposalArea
from .geometries import Coordinates, Boundry


@dataclass
class AddEmployReq:
    fname: str
    lname: str
    address: str
    contacts: Iterable[str]
    office_id: uuid.UUID


@dataclass
class DriverBase:
    fname: str
    lname: str
    address: str
    contact: str
    office_id: uuid.UUID
    vehicle_id: uuid.UUID


@dataclass
class MakeEmployDriverForOffice:
    employ_id: uuid.UUID
    office_id: uuid.UUID
    vehicle_id: uuid.UUID|None


@dataclass
class AssignVehicleToDriver:
    driver_id: uuid.UUID
    vehicle_id: uuid.UUID


@dataclass
class CreateDriverReq(DriverBase):
    vehicle_id: uuid.UUID
    username: str
    password: str


@dataclass
class DriverCreatedRes(CreateDriverReq):
    id: uuid.UUID


@dataclass
class DeleteDriverReq:
    id: uuid.UUID


@dataclass
class DriverDeletedRes:
    status: bool


@dataclass
class AddDriverToOfficeReq(DriverBase):
    ...


@dataclass
class AddVehicleReq:
    plate_no: str
    office_id: uuid.UUID = None


@dataclass
class VehicleAddedRes:
    Vehicle: Vehicle


@dataclass
class RemoveVehicleReq:
    id: uuid.UUID


@dataclass
class VehicleRemovedRes:
    status: bool
    vehicle: Vehicle


@dataclass
class AddWDAReq:
    name: str
    location: Coordinates
    area: int


@dataclass
class AddOfficeReq:
    area_name: str
    wda_id: uuid.UUID
    boundry_coordinates: Boundry
    terminal_location: Coordinates


@dataclass
class AddOfficeAndWda:
    area_name: str
    wda_location: Coordinates
    wda_area: int
    bounded_area: Boundry



@dataclass 
class AddOfficeAndWdaRes:
    office: Office
    wda: WastDisposalArea



@dataclass
class GetVehicleLocationReq:
    id: uuid.UUID


@dataclass
class VehicleLocation:
    location: Coordinates


@dataclass
class SetVehicleLocationReq:
    vehicle_id: uuid.UUID
    location: Coordinates


@dataclass
class VehicleLocationChangedRes:
    status: bool
    location: Coordinates


@dataclass
class InstallDBinReq:
    name: str
    identifier: str
    office_id: uuid.UUID
    location: Coordinates
    depth: float


@dataclass
class DBinInstalledRes:
    dbin: DustBin


@dataclass
class GetDBinReq:
    by_id: Optional[uuid.UUID]
    by_location: Coordinates


@dataclass
class ChangeDbinLevelReq:
    id: uuid.UUID
    level: float


@dataclass
class AddUserReq:
    # employ_id: uuid.UUID
    username: str
    password: str
    role: str
    driver_id: uuid.UUID|None







