from flask import Blueprint, jsonify

from .auth import auth
import src.use_cases.drivers as uc_driver

drivers_bp = Blueprint("drivers", __name__)


@drivers_bp.get("/")
@auth
def _get_all_drivers(current_user):
    drivers = uc_driver.all_drivers(current_user)
    result = [{
        "id": dv.id,
        "fname": dv.fname,
        "lname": dv.lname,
        "address": dv.address, 
        "contact": dv.contact,
        "office_id": dv.office_id,
        "vehicle_id": dv.vehicle_id
    } for dv in drivers]

    return jsonify(result)


