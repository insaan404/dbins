import abc
import uuid
from .geometries import Coordinates, Boundry



class Entity(abc.ABC):
	def __init__(self, id: uuid.UUID):
		self.id = id


class Driver(Entity):
	def __init__(
		self,
		id: uuid.UUID,
		fname: str,
		lname: str,
		address: str,
		contact: str,
		office_id: uuid.UUID,
		vehicle_id: uuid.UUID,
	):
		super().__init__(id)
		self.fname = fname
		self.lname = lname
		self.address = address
		self.contact = contact
		self.office_id = office_id
		self.vehicle_id = vehicle_id


class Vehicle(Entity):
	def __init__(
		self,
		id: uuid.UUID,
		plate_no: str,
		current_location: Coordinates | None,
		office_id: uuid.UUID,
	):
		super().__init__(id)
		self.plate_no = plate_no
		self.current_location = current_location
		self.office_id = office_id
		self._is_moving = False

	@property
	def is_moving(self):
		return self._is_moving

	def start_moving(self):
		self._is_moving = True

	def set_location(self, location: Coordinates):
		self.current_location = location


class WastDisposalArea(Entity):
	def __init__(self, id: uuid.UUID, name: str, location: Coordinates, area: int):
		super().__init__(id)

		self.name = name
		self.location = location
		self.area = area


class Office(Entity):
	@classmethod
	def new(cls, area_name: str, boundry_coordinates: Boundry, wda_id: uuid.UUID, termial: Coordinates):
		return cls(uuid.uuid4(), area_name, boundry_coordinates, wda_id, termial)

	def __init__(
		self,
		id: uuid.UUID,
		area_name: str,
		boundry: Boundry,
		wda_id: uuid.UUID,
		terminal_location: Coordinates
	):
		super().__init__(id)

		self.area_name = area_name
		self.wda_id = wda_id
		self.boundry = boundry
		self.terminal_location = terminal_location


class DustBin(Entity):
	def __init__(self, id: uuid.UUID, name:str, identifier: str, location: Coordinates,
	      	depth: float, office_id: uuid.UUID, ):
		super().__init__(id)
		self.name = name
		self.location = location
		self.depth = depth
		self.identifier = identifier
		self._level = 0
		self.office_id = office_id

	@property
	def level(self):
		return self._level

	def set_level(self, level: float):
		if level > self.depth:
			self._level = self.depth
		else:
			self._level = level

	@property
	def level_status(self):
		if self._level == 0:
			return 0
		return (self._level/self.depth)*100
	






	
