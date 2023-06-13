import os
import uuid

import jwt

from src.models.adminstration import User
import src.use_cases.administration as uc_admin


def create_token(user):
    token = jwt.encode({"user": user.id.hex}, os.getenv("key"), algorithm="HS256")
    return token


def decode_token(token) -> User|None:
    print("this-> ", token)
    try:
        payload = jwt.decode(token, os.getenv("key"), algorithms=["HS256"])

        uid = uuid.UUID(payload["user"])
        user = uc_admin.get_auth_user(uid)
        print(user)
        return user
    except jwt.DecodeError:
        return None

