import uuid
import pathlib
import os
import dotenv

from sqlalchemy import create_engine

from src.models.adminstration import User
from src.data_access.sql_models import Base

dotenv.load_dotenv()
DATA_DIR = pathlib.Path("./data").absolute()
db_path = DATA_DIR.joinpath(pathlib.Path("./database.db")) 
engine = create_engine(f"sqlite:///{db_path}")
Base.metadata.create_all(engine)


from src.data_access.sqlit_repos import (
    user_repo
)


user = User(uuid.uuid4(), "root@root.com", "kombot99", "root")
user_repo.add(user)


print("data inserted!")







