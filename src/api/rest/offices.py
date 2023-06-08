import uuid
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from sqlalchemy.exc import IntegrityError


from src.models.requests_responses import (AddOfficeReq, AddOfficeAndWda, )

import src.use_cases.administration as uc_admin
import src.use_cases.office as uc_office
import src.use_cases.drivers as uc_driver
import src.use_cases.vehicle as uc_vhl
import src.use_cases.dbin as uc_dbin
import src.use_cases.wda as uc_wda
from src.models.models import Boundry
from src.models.geometries import Coordinates
import src.models.requests_responses as rp

from .auth import auth


office_bp = Blueprint("offices", __name__)


@office_bp.post("/")
@auth
def _add_office(current_user):
    data = request.json
    bd_area = Boundry(
            [Coordinates(crd['lat'], crd['lng']) for crd in data["office"]["boundry_coordinates"]]
        )
    try:
        if not "wda" in data:
            off = data["office"]
            req = AddOfficeReq(off["area_name"], uuid.UUID(off["wda_id"]), bd_area)
            office = uc_admin.add_office(current_user, req)
            return jsonify({
                "id": office.id.hex,
                "area_name": office.area_name,
                "boundry": office.boundry.to_dict(),
                "terminal_location": office.terminal_location.to_dict()
            })
        
        else:
            off = data["office"]
            wda = data["wda"]
            wlc = wda["location"]
            req = AddOfficeAndWda(
                off["area_name"], Coordinates(wlc["lat"], wlc["lng"]), wda["area"], bd_area
            )

            resp = uc_admin.add_office_and_wda(current_user, req)
            office = resp.office
            wda = resp.wda

            return jsonify({
                "office": {
                    "id": office.id.hex,
                    "area_name": office.area_name,
                    "boundry": office.boundry.to_dict()
                },
                "wda": {
                    "id": wda.id.hex,
                    "location": {
                        "lat": wda.location.lat,
                        "lng": wda.location.lng
                    },
                    "area": wda.area
                }
            })
    except IntegrityError:
        return jsonify({"msg": "integrity error"})


@office_bp.get("/")
@cross_origin()
@auth
def _get_offices(current_user):
    offcs = uc_office.get_all_offices(current_user)
    resp = [
        {
            "id": off.id,
            "area_name": off.area_name,
            "wda_id": off.wda_id,
            "boundry": off.boundry.to_dict(),
            "terminal_location": off.terminal_location.to_dict()
        }
        for off in offcs
    ]

    return jsonify(resp)


@office_bp.post("/<id>/drivers")
@auth
def _add_driver_to_office(current_user, id):
    d = request.json
    req = rp.CreateDriverReq(
        d["fname"], d["lname"], d["address"], d["contact"], uuid.UUID(id), uuid.UUID(d["vehicle_id"])
    )
    dv = uc_admin.add_driver(current_user, req)
    return jsonify({
        "id": dv.id,
        "fname": dv.fname,
        "lname": dv.lname,
        "address": dv.address, 
        "contacts": dv.contact,
        "office_id": dv.office_id,
        "vehicle_id": dv.vehicle_id
    })


@office_bp.get("/<id>/drivers")
@auth
def _get_office_drivers(current_user, id):
    drivers = uc_driver.get_office_drivers(current_user, uuid.UUID(id))
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


@office_bp.get("/<id>/vehicles")
@auth
def _get_office_vehicles(current_user, id):
    vhls = uc_vhl.get_office_vehicles(current_user, uuid.UUID(id))
    result = [{
        "id": vhl.id,
        "plate_no": vhl.plate_no,
        "office_id": vhl.office_id,
        "is_moving": vhl.is_moving,
        "current_location": {
            "lat":  vhl.current_location.lat if vhl.current_location else None,
            "lng": vhl.current_location.lng if vhl.current_location else None
        }
    } for vhl in vhls]

    return jsonify(result)


@office_bp.post("/<id>/vehicles")
@auth
def _add_vehicle_to_office(current_user, id):
    vh = request.json
    loc = vh.get("location")
    loc = loc if loc else None
    req = rp.AddVehicleReq(vh["plate_no"], loc, uuid.UUID(id))
    v = uc_admin.add_vehicle(current_user, req)    
    return jsonify({
        "id": v.id,
        "plate_no": v.plate_no,
        "office_id": v.office_id,
        "current_location": {
            "lat":  v.current_location.lat if v.current_location else None,
            "lng": v.current_location.lng if v.current_location else None
        }
    })


@office_bp.get("/<id>/wda")
@auth
def _get_office_wda(current_user, id):
    print("getting: ", id)
    wda = uc_wda.get_office_wda(current_user, uuid.UUID(id))
    return jsonify(
        {"id": wda.id,
        "name": wda.name,
        "location": {
            "lat": wda.location.lat,
            "lng": wda.location.lng
        }})

@office_bp.get("/<id>")
@auth
def _get_office(current_user, id: str):
    office = uc_office.get_by_id(current_user, uuid.UUID(id))
    return jsonify({
        "id": office.id,
        "area_name": office.area_name,
        "wda_id": office.wda_id,
        "boundry": office.boundry.to_dict(),
        "terminal_location": office.terminal_location.to_dict()
    })


# @office_bp.get("/<id>/employs")
# @auth
# def _get_office_employs(current_user, id):
#     emps = uc_employ.get_office_employs(current_user, uuid.UUID(id))
#     result = []
#     for emp in emps:
#         result.append({
#             "id": emp.id,
#             "fname": emp.fname,
#             "lname": emp.lname,
#             "address": emp.address, 
#             "contact": emp.contact,
#             "office_id": emp.office_id
#         })
#     return jsonify(result)


@office_bp.get("/<id>/dbins")
@auth
def _get_office_dbins(current_id, id):
    dbins = uc_dbin.get_office_dbins(current_id, uuid.UUID(id))
    loc = lambda lc: {"lat": lc.lat, "lng": lc.lng}
    result = [{
        "id": dbin.id,
        "name": dbin.name,
        "level": dbin.level,
        "office_id": dbin.office_id,
        "depth": dbin.depth,
        "location": loc(dbin.location),
        "level_status": dbin.level_status
    } for dbin in dbins]

    return jsonify(result)


@office_bp.get("/<office_id>/dbins/<id>")
@auth
def _get_office_dbin(current_user, office_id, id):
    dbin = uc_dbin.get_dustbin(current_user, uuid.UUID(id))

    return jsonify({
        "id": dbin.id,
        "name": dbin.name,
        "level": dbin.level,
        "office_id": dbin.office_id,
        "depth": dbin.depth,
        "location": {"lat": dbin.location.lat, "lng": dbin.location.lng},
        "level_status": dbin.level_status
    })


@office_bp.post("/<office_id>/dbins")
@auth
def _install_dbin(current_user, office_id):
    dbin = request.json
    # dm = Dimensions(bin["dimensions"]["height"], bin["dimensions"]["volume"])
    depth = dbin["depth"]
    loc = Coordinates(dbin["location"]["lat"], dbin["location"]["lng"])
    req = rp.InstallDBinReq(dbin["name"], dbin["identifier"], uuid.UUID(dbin["office_id"]),
                            loc, depth)
    dbin = uc_dbin.install_dustbin(current_user, req)

    return jsonify({
        "id": dbin.id,
        "name": dbin.name,
        "level": dbin.level,
        "office_id": dbin.office_id,
        "depth": dbin.depth,
        "location": {"lat": dbin.location.lat, "lng": dbin.location.lng},
        "level_status": dbin.level_status
 
    }) 




    

