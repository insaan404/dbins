from typing import Iterable, Optional
import uuid
from enum import Enum
import datetime

from .models import Entity


class Role(str, Enum):
    ROOT = "root"
    DRIVER = "driver"


class User(Entity):
    def __init__(
        self,
        id: uuid.UUID,
        username: str,
        password: str,
        role: Role,
        driver_id: uuid.UUID|None=None
    ):
        super().__init__(id)

        self.username = username
        self.password = password
        self.role = role
        self.driver_id = driver_id


class TaskStatus(str, Enum):
    PENDING = "pending"
    FULFILLED = "fulfilled"
    PASSED = "passed"


class CleanDustBinTask:
    id: uuid.UUID
    dbin_id: uuid.UUID
    user_id: uuid.UUID
    task_status: TaskStatus
    assigned_at: datetime.datetime
    parent: Optional["CleanDustBinTask"] = None

    def __init__(self, id: uuid.UUID, t_status: TaskStatus, assigned_at: datetime.datetime,
            user_id: uuid.UUID, dbin_id: uuid.UUID, parent: "CleanDustBinTask" = None):
        self.id = id
        self.dbin_id = dbin_id
        self.task_status = t_status
        self.assigned_at = assigned_at
        self.user_id = user_id
        self.parent = parent








