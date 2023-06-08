import re
import uuid
from flask import Blueprint, jsonify, request


from src.models.adminstration import Role, User
from .auth import auth
import src.models.requests_responses as rp
import src.use_cases.administration as uc_admin
import src.use_cases.drivers as uc_driver
users_bp = Blueprint("users", __name__)


@users_bp.get("/")
@auth
def _get_all_users(current_user):
    users = uc_admin.get_all_users(current_user)
    result = [{
        "id": usr.id,
        "username": usr.username,
        "role": usr.role} for usr in users]

    return jsonify(result)


@users_bp.get("/office")
@auth
def _get_user_office(current_user):
    office = uc_admin.get_user_office(current_user)
    return jsonify({
        "id": office.id,
        "area_name": office.area_name,
        "wda_id": office.wda_id,
        "boundry": office.boundry.to_dict(),
        "terminal_location": office.terminal_location.to_dict()
    })


@users_bp.get("/me")
@auth
def _get_me(current_user):
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "driver_id": current_user.driver_id
    })

@users_bp.get("/me/driver")
@auth
def _get_me_driver(current_user: User):
    if current_user.role == Role.ROOT:
        return jsonify()
    dv = uc_driver.get_driver(current_user, current_user.driver_id)
    return jsonify({
        "id": dv.id,
        "fname": dv.fname,
        "lname": dv.lname,
        "address": dv.address, 
        "contact": dv.contact,
        "office_id": dv.office_id,
        "vehicle_id": dv.vehicle_id}
        )


@users_bp.get("/<id>")
@auth
def _get_all_user(current_user, id):
    usr = uc_admin.get_user(current_user, uuid.UUID(id))
    return jsonify({
        "id": usr.id,
        "username": usr.username,
        "role": usr.role,
        "driver_id": usr.driver_id
    })


@users_bp.post("/")
@auth
def _add_user(current_user):
    u = request.json
    req = rp.AddUserReq(uuid.uuid4(), u["username"], u["password"], u["role"], u.get("driver_id"))
    usr = uc_admin.add_user(current_user, req)
    
    return jsonify({
        "id": usr.id,
        "username": usr.username,
        "role": usr.role,
        "driver_id": usr.driver_id
    })
