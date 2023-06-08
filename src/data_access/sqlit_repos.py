import os
import uuid
import re
from typing import Iterable, Callable
import abc
from sqlalchemy.orm import Session as SqSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, create_engine

from ..models.geometries import Coordinates, Boundry
from ..models.adminstration import User, Role, CleanDustBinTask
from ..models.models import (Office, Vehicle, Driver, WastDisposalArea,
                            DustBin)


import src.data_access.sql_models as sms

session_factory: Callable[..., SqSession] = None


def init_sqlit_repositories():
    global session_factory
    engine = create_engine(os.getenv("db"))
    session_factory = sessionmaker(engine)


init_sqlit_repositories()


def _coordinates_to_db_form(cord: Coordinates):
    return f"({cord.lat}, {cord.lng})"


def coodrinates_from_str(string: str):
    string = string[1:-1]
    lat, lng = string.split(",")
    return Coordinates(float(lat), float(lng))


def _coordinates_from_tups(tup: tuple[str, str]):
    lat, lng = tup
    return Coordinates(float(lat), float(lng))


def bounded_area_from_str(string: str):
    pattern = r"\(([-+]?\d+(?:\.\d+)?),\s*([-+]?\d+(?:\.\d+)?)\)"
    lst = re.findall(pattern, string)
    rslt = [_coordinates_from_tups(tp) for tp in lst]
    return Boundry(rslt)


def boundry_to_str(bd: Boundry):
    cords = bd.coordinates
    cords_str = (_coordinates_to_db_form(cord) for cord in cords)
    return "["+ ",".join(cords_str) + "]"




# def dimensions_to_str(dim: Dimensions):
#     return f"({dim.height}, {dim.volume})"


# def str_to_dimensions(string: str):
#     string = string[1:-1]
#     h, v = string.split(",")
#     return Dimensions(float(h), float(v))


class SqlitRepository(abc.ABC):

    def __init__(self):
        self.cache: Iterable = []

        self._init_cache()

    def remove_from_cache(self, obj):
        data = list(self.cache)
        data.remove(obj)
        self.cache = data

    def add_to_cache(self, obj):
        data = list(self.cache)
        data.append(obj)

        self.cache = data


class OfficeRepository(SqlitRepository):
    cache: Iterable[Office]

    def _init_cache(self):
        session = session_factory()
        result = session.scalars(select(sms.Office)).all()
        for o in result:
            bd = bounded_area_from_str(o.boundry)
            self.cache.append(
                Office(o.id, o.area_name, bd, o.wda_id, coodrinates_from_str(o.terminal_location))
            )
        session.close()
        
    def add(self, office: Office) -> bool:

        bd_str = boundry_to_str(office.boundry)
        off = sms.Office(id=office.id, area_name=office.area_name, wda_id = office.wda_id, boundry=bd_str,
                        terminal_location=_coordinates_to_db_form(office.terminal_location))
        session = session_factory()

        session.add(off)
        session.commit()
        session.close()

        self.cache.append(office)


    def remove(self, office: Office) -> bool:
        session = session_factory()

        off = session.get(sms.Office, office.id)
        session.delete(off)

        session.commit()
        session.close()
        self.cache.remove(office)

    def _get(self, id: uuid.UUID) -> Office:
        for off in self.cache:
            if off.id == id:
                return off

    def get(self, id: uuid.UUID) -> Office:
        return self._get(id)

        
    def get_all(self) -> Iterable[Office]:
        return self.cache
      

class VehicleRepository(SqlitRepository):

    def _init_cache(self):
        session = session_factory()
        result = session.scalars(select(sms.Vehicle)).all()
        for v in result:
            self.cache.append(
                Vehicle(v.id, v.plate_no, None, v.office_id)
            )
        session.close()

    def add(self, vehicle: Vehicle) -> bool:
        
        with session_factory() as session:
            veh = sms.Vehicle(id=vehicle.id, plate_no=vehicle.plate_no, office_id=vehicle.office_id)
            session.add(veh)
            session.commit()
        self.cache.append(vehicle)
            
    def remove(self, id: uuid.UUID) -> bool:
        with session_factory() as session:
            veh = session.get(sms.Vehicle, id)
            session.delete(veh)
            session.commit()


    def get(self, id: uuid.UUID) -> Vehicle:
        for vh in self.cache:
            if vh.id == id:
                return vh


    def get_all(self) -> Iterable[Vehicle]:
        return self.cache


# class EmployRepository(SqlitRepository):

#     def _init_cache(self):
#         session = session_factory()
#         result = session.scalars(select(sms.Employ)).all()
#         for e in result:
#             self.cache.append(
#                 Employ(e.id, e.fname, e.lname, e.address, e.contact, e.office_id)
#             )
#         session.close()

#     def add(self, emp: Employ) -> bool:
#         with session_factory() as session:
#             e = sms.Employ(
#                 id=emp.id, fname=emp.fname, lname=emp.lname, address=emp.address,
#                 contact=emp.contact, office_id=emp.office_id)
#             session.add(e)
#             session.commit()
#         self.cache.append(emp)

#     def remove(self, id: uuid.UUID) -> bool:
#         with session_factory() as session:
#             e = session.get(sms.Employ, id)
#             session.delete(e)
#             session.commit()

#     def get(self, id: uuid.UUID) -> Employ:
#         for emp in self.cache:
#             if emp.id == id:
#                 return emp

#     def get_all(self) -> Iterable[Employ]:
#         return self.cache
    
#     def update_cache_with(self, id: uuid.UUID) -> None:
#         with session_factory() as session:
#             e = session.get(sms.Employ, id)
#         self.cache.append(
#             Employ(e.id, e.fname, e.lname, e.address, e.contact, e.office_id)
#         )



class DriverRepository(SqlitRepository):

    def _init_cache(self):
        session = session_factory()
        result = session.scalars(select(sms.Driver)).all()
        for d in result:
            self.cache.append(
                Driver(d.id, d.fname, d.lname, d.address, d.contact, d.office_id, d.vehicle_id)
            )
        session.close()

    def add(self, driver: Driver) -> bool:
        with session_factory() as session:
            d = sms.Driver(
                id=driver.id, fname=driver.fname, lname=driver.lname, address=driver.address,
                contact=driver.contact, office_id=driver.office_id, vehicle_id=driver.vehicle_id)
            
            session.add(d)
            session.commit()
        self.cache.append(driver)

    def remove(self, id: uuid.UUID) -> bool:
        with session_factory() as session:
            d = session.get(sms.Driver, id)
            session.delete(d)
            session.commit()

    def get(self, id: uuid.UUID) -> Driver:
        for d in self.cache:
            if d.id == id:
                return d

    def get_all(self) -> Iterable[Driver]:
        return self.cache

class WDARepository(SqlitRepository):

    def _init_cache(self):
        session = session_factory()
        result = session.scalars(select(sms.WastDisposalArea)).all()
        for w in result:
            self.cache.append(
                 WastDisposalArea(w.id, w.name, coodrinates_from_str(w.location), w.area)
            )
        session.close()

    def add(self, wda: WastDisposalArea) -> bool:
        with session_factory() as session:
            loc = _coordinates_to_db_form(wda.location)
            w = sms.WastDisposalArea(id=wda.id, name=wda.name, location=loc, area=wda.area)
            session.add(w)
            session.commit()

        self.cache.append(wda)

    def remove(self, id: uuid.UUID) -> bool:
        with session_factory() as session:
            w = session.get(sms.WastDisposalArea, id)
            session.delete(w)
            session.commit()

    def get(self, id: uuid.UUID) -> WastDisposalArea:
        for wda in self.cache:
            if wda.id == id:
                return wda
    def get_all(self) -> Iterable[WastDisposalArea]:
        return self.cache


class DustBinRepository(SqlitRepository):

    def _init_cache(self):
        session = session_factory()
        result = session.scalars(select(sms.DustBin)).all()
        for db in result:
            crd = coodrinates_from_str(db.location)
            self.cache.append(
                DustBin(db.id, db.name, db.identifier, crd, db.depth, db.office_id)
            )
        session.close()

    def add(self, dbin: DustBin) -> bool:
        with session_factory() as session:
            loc = _coordinates_to_db_form(dbin.location)
            db = sms.DustBin(id=dbin.id, name=dbin.name, identifier=dbin.identifier, location=loc,
                            depth=dbin.depth, office_id=dbin.office_id)
            session.add(db)
            session.commit()
        self.cache.append(dbin)

    def remove(self, id: uuid.UUID) -> bool:
        with session_factory() as session:
            db = session.get(sms.DustBin, id)
            session.delete(db)
            session.commit()

    def get(self, id: uuid.UUID) -> DustBin:
        for dbin in self.cache:
            if dbin.id == id:
                return dbin

    def get_all(self) -> Iterable[DustBin]:
        return self.cache




class UserRepository(SqlitRepository):

    def _init_cache(self):
        session = session_factory()
        result = session.scalars(select(sms.User)).all()
        for u in result:
            user = User(u.id, u.username, u.password, u.role, u.driver_id)
            self.cache.append(user)
        self.cache = result 
        session.close()

    def add(self, user: User) -> bool:
        with session_factory() as session:
            d = sms.User(id=user.id, username=user.username, password=user.password,
                         role=user.role, driver_id=user.driver_id)
            
            session.add(d)
            session.commit()

        self.cache.append(user)

    def remove(self, id: uuid.UUID) -> bool:
        with session_factory() as session:
            d = session.get(sms.User, id)
            session.delete(d)
            session.commit()
        # change


    def get(self, id: uuid.UUID) -> User:
        for user in self.cache:
            if user.id == id:
                return user

    def get_all(self) -> Iterable[User]:
        return self.cache


class TaskRepository(SqlitRepository):
 
    def _init_cache(self):
        with session_factory () as session:
            session = session_factory()
            results = session.scalars(select(sms.CleanDustBinTask)).all()
        
        for u in results:
            task = CleanDustBinTask(u.id, u.task_status, u.assigned_at, u.user_id, u.dbin_id, u.parent)
            self.cache.append(task)  

    def add(self, task: CleanDustBinTask):
        with session_factory() as session:
            t = sms.CleanDustBinTask(id=task.id, task_status=task.task_status, assigned_at=task.assigned_at,
                                     user_id=task.user_id, dbin_id=task.dbin_id, parent_id=task.parent.id)
            session.add(t)
            session.commit()

    def remove(self, id: uuid.UUID):
        with session_factory() as session:
            t = session.get(sms.Task, id)
            session.delete(t)
            session.commit()

    def get(self, id: uuid.UUID):
        with session_factory() as session:
            t = session.get(sms.Task, id)

        return CleanDustBinTask(t.id, t.task_status, t.assigned_at, t.user_id, t.dbin_id, t.parent)

    def get_all(self):
        with session_factory() as session:
            data = session.scalar(select(sms.Task)).all()
        for t in data:
            yield 



wda_repo = WDARepository()
office_repo = OfficeRepository()
user_repo = UserRepository()
# emp_repo = EmployRepository()
driver_repo = DriverRepository()
task_repo = TaskRepository()
dbin_repo = DustBinRepository()
vehicle_repo = VehicleRepository()


