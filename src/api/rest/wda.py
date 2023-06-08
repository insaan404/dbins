import uuid
from flask import Blueprint, jsonify, request

from .auth import auth
from src.models.geometries import Coordinates
import src.models.requests_responses as rp

import src.use_cases.wda as uc_wda


wda_bp = Blueprint("wdas", __name__)



@wda_bp.route("/", methods=["POST"])
@auth
def _add_wda(current_user):
    data = request.json
    loc = data["location"]
    rq = rp.AddWDAReq(data["name"], Coordinates(loc["lat"], loc["lng"]), data["area"])
    res = uc_wda.add_wda(current_user, rq)

    return jsonify({
        "id": res.id,
        "name": res.name,
        "location": {
            "lat": res.location.lat,
            "lng": res.location.lng
        },
        "area": res.area
    })    


@wda_bp.get("/")
@auth
def _get_wdas(current_user):
    wdas = uc_wda.get_all(current_user)
    result = []
    for wda in wdas:
        result.append({
        "id": wda.id,
        "name": wda.name,
        "location": {
            "lat": wda.location.lat,
            "lng": wda.location.lng
        },
        "area": wda.area
    })
    return jsonify(result)


@wda_bp.get("/<id>")
@auth
def _get_wda(current_user, id):
    res = uc_wda.get_wda(current_user, uuid.UUID(id))
    return jsonify({
        "id": res.id,
        "name": res.name,
        "location": {
            "lat": res.location.lat,
            "lng": res.location.lng
        },
        "area": res.area
    })

