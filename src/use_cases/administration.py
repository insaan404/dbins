import uuid

from ..models.adminstration import User, Role
from ..models.requests_responses import (
    DriverCreatedRes,
    CreateDriverReq,
    DeleteDriverReq,
    AddVehicleReq,
    RemoveVehicleReq,
    AddOfficeReq,
    AddUserReq,
    AddOfficeAndWda,
    AddOfficeAndWdaRes,
)

from ..models.models import WastDisposalArea, Office, Vehicle, Driver
from ..data_access.sqlit_repos import (office_repo, dbin_repo, driver_repo as drv_repo,
                                       user_repo, wda_repo, vehicle_repo as veh_repo )


class PrivilageError(Exception):
    pass


# def add_employ(user: User, req: AddEmployReq) -> Employ:
#     if user.role != Role.ROOT:
#         raise PrivilageError()
    
#     emp = Employ(uuid.uuid4(), req.fname, req.lname, req.address, req.contacts, req.office_id)
    
#     emp_repo.add(emp)
#     return emp

# def remove_employ(user: User, id: uuid) -> bool:
#     if user.role != Role.ROOT:
#         raise PrivilageError()
    
#     emp = emp_repo.get(id)
#     return emp_repo.remove(emp)


def add_user(user: User, req: AddUserReq) -> User:
    if user.role != Role.ROOT:
        raise PrivilageError()

    usr = User(uuid.uuid4(), req.username, req.password, req.role, req.driver_id)

    resp = user_repo.add(usr)
    return usr


def remove_user(user: User, id: uuid.UUID) -> bool:
    if user.role != Role.ROOT:
        raise PrivilageError()

    usr = user_repo.get(id)
    return user_repo.remove(usr)


def get_auth_user(id: uuid.UUID) -> User:
    print("id: here: ", id)
    return user_repo.get(id)


def get_user(user: User, id: uuid.UUID) -> User:
    usr = user_repo.get(id)
    if user.id == id or user.role == Role.ROOT:
        return usr



def get_user_by_username(username: str) -> User:
    users = user_repo.get_all()
    for user in users:
        if user.username == username:
            return user
        

def get_all_users(user: User):
    if user.role != Role.ROOT:
        raise PrivilageError()

    return user_repo.get_all()
   


def add_driver(user: User, req: CreateDriverReq) -> DriverCreatedRes:
    if user.role != Role.ROOT:
        raise PrivilageError()

    uid = uuid.uuid4()
    d = Driver(
        uid,
        req.fname,
        req.lname,
        req.address,
        req.contact,
        req.office_id,
        req.vehicle_id,
    )
    
    drv_repo.add(d)
    user = User(uuid.uuid4(), uid, req.username, req.password, Role.DRIVER)
    user = User(uuid.uuid4(), req.username, req.password, Role.DRIVER, uid)
    user_repo.add(user)
    return d


def remove_driver(user: User, req: DeleteDriverReq) -> bool:
    if user.role != Role.ROOT:
        raise PrivilageError()

    return drv_repo.remove(req.id)
    



def add_vehicle(user: User, req: AddVehicleReq) -> Vehicle:
    if user.role != Role.ROOT:
        raise PrivilageError()
    v = Vehicle(uuid.uuid4(), req.plate_no, '', req.office_id)
    veh_repo.add(v)
    return v


def remove_vehicle(user: User, req: RemoveVehicleReq) -> bool:
    if user.role != Role.ROOT:
        raise PrivilageError()

    return veh_repo.remove(req.id)


def add_office(user: User, req: AddOfficeReq) -> Office:
    if user.role != Role.ROOT:
        raise PrivilageError()

    o = Office.new(req.area_name, req.boundry_coordinates, req.wda_id, req.terminal_location)
    office_repo.add(o)
    return o
    

def add_office_and_wda(user: User, req: AddOfficeAndWda) -> AddOfficeAndWdaRes:
    if user.role != Role.ROOT:
        raise PrivilageError()
    
    wda = WastDisposalArea(uuid.uuid4(), req.wda_location, req.wda_area)
    office = Office.new(req.area_name, req.bounded_area, wda.id)
    wda_repo.add(wda)
    office_repo.add(office)

    return AddOfficeAndWdaRes(office, wda)



def get_user_office(user: User) -> Office:
    if user.role == Role.ROOT:
        return 
    driver = drv_repo.get(user.driver_id)
    office = office_repo.get(driver.office_id)

    return office












