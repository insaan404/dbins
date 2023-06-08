import uuid

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError


from .auth import auth
from src.models.requests_responses import (AddEmployReq)
import src.use_cases.administration as uc_admin
import use_cases.__employs as uc_employ



employ_bp = Blueprint("employs", __name__)


@employ_bp.post("/")
@auth
def _add_employ(current_user):
    data = request.json
    req = AddEmployReq(
        data["fname"], data["lname"], data["address"], data["contact"],
        uuid.UUID(data["office_id"])
    )

    try:
        emp = uc_admin.add_employ(current_user, req)

        return jsonify({
            "id": emp.id,
            "fname": emp.fname,
            "lname": emp.lname,
            "address": emp.address, 
            "contacts": emp.contact,
            "office_id": emp.office_id
        })
    except IntegrityError:
        return jsonify({"msg": "integrity error"})
    

@employ_bp.get("/<id>")
@auth
def _get_employ(current_user, id):
    emp = uc_employ.get_employ(current_user, uuid.UUID(id))

    return jsonify({
        "id": emp.id,
        "fname": emp.fname, 
        "lname": emp.lname,
        "address": emp.address, 
        "contacts": emp.contact,
        "office_id": emp.office_id
    })


@employ_bp.get("/")
@auth
def _get_all_employs(current_user):
    emps = uc_employ.get_all(current_user)

    return jsonify([
        {"id": e.id, "fname": e.fname, "lname": e.lname, "address": e.address,
        "contacts": e.contact, "office_id": e.office_id}
    for e in emps])
