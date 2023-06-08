import enum
from flask import Blueprint, jsonify, request

import src.use_cases.administration as uc_admin
from src.api.rest.dbins import dbin_bp
from src.api.rest.drivers import drivers_bp
from src.api.rest.offices import office_bp
from src.api.rest.users import users_bp
from src.api.rest.wda import wda_bp
from src.common.auth_utils import create_token
from src.data_access.sql_models import Driver, User
from src.models.adminstration import Role


class Device(str, enum.Enum):
    MOBILE = "mobile"
    WEBAPP = "webapp"


api = Blueprint("api", __name__)
api.register_blueprint(office_bp, url_prefix="/offices")
api.register_blueprint(drivers_bp, url_prefix="/drivers")
api.register_blueprint(dbin_bp, url_prefix="/dbins")
api.register_blueprint(wda_bp, url_prefix="/wdas")
api.register_blueprint(users_bp, url_prefix="/users")



@api.post("/login")
def _login():
    
    cred = request.json
    user = uc_admin.get_user_by_username(cred["username"])
    device = cred.get("device")
    if device != Device.MOBILE and user.role == Role.DRIVER:
        return jsonify({"msg": " driver must login using mobile app "})      
    if not user:
        return jsonify({"msg": "wrong username"})
    if user.password == cred["password"]:
        token = create_token(user)
        return jsonify({"token": token})
    else:
        return jsonify({"msg": "wrong credentials"})





