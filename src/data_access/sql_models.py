import uuid
from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import ForeignKey

from ..models.adminstration import Role, TaskStatus, CleanDustBinTask



class Base(DeclarativeBase):
    pass



class Driver(Base):
    __tablename__ = "driver"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    fname: Mapped[str]
    lname: Mapped[str]
    address: Mapped[str]
    contact: Mapped[str]
    vehicle_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("vehicle.id"), nullable=True)
    office_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("office.id"), nullable=True)

    office: Mapped["Office"] = relationship(back_populates="drivers")


class Vehicle(Base):
    __tablename__ = "vehicle"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    plate_no: Mapped[str] = mapped_column(unique=True)
    office_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("office.id"), nullable=False)

    office: Mapped["Office"] = relationship(back_populates="vehicles")


class WastDisposalArea(Base):
    __tablename__ = "wda"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    location: Mapped[str]
    area: Mapped[int]



class Office(Base):
    __tablename__ = "office"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    area_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    wda_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("wda.id"))
    terminal_location: Mapped[str]

    boundry: Mapped[str]

    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="office")
    dustbins: Mapped[list["DustBin"]] = relationship(back_populates="office")
    drivers: Mapped[list[Driver]] = relationship(back_populates="office")


class DustBin(Base):
    __tablename__ = "dustbin"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    identifier: Mapped[str] = mapped_column(unique=True, nullable=False)
    location: Mapped[str]   
    depth: Mapped[float]
    office_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("office.id"))
    
    office: Mapped["Office"] = relationship(back_populates="dustbins")



class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    role: Mapped[Role]
    driver_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("driver.id"), nullable=True)

    driver: Mapped["Driver"] = relationship()
    tasks: Mapped["CleanDustBinTask"] = relationship(back_populates="user", collection_class=list)


class CleanDustBinTask(Base):
    __tablename__ = "task"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    task_status: Mapped[TaskStatus]
    assigned_at: Mapped[datetime]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    dbin_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dustbin.id"))
    parent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("task.id"), nullable=True)

    user: Mapped["User"] = relationship(back_populates="tasks")
    parent: Mapped["CleanDustBinTask"] = relationship(remote_side=[id])












