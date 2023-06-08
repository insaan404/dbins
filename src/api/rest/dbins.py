from flask import Blueprint, request, jsonify

from .auth import auth
import src.use_cases.dbin as uc_dbin

dbin_bp = Blueprint("dbin", __name__)



@dbin_bp.post("/level")
def _set_dbin_level():
    dta = request.json
    res = uc_dbin.change_dbin_level(dta["identifier"], dta["level"])
    return jsonify({"message": res})


@dbin_bp.get("/")
@auth
def _get_all_dbins(current_user):
    dbins = uc_dbin.get_all_dustbins(current_user)
    loc = lambda lc: {"lat": lc.lat, "lng": lc.lng}
    result = [{
        "id": dbin.id,
        "name": dbin.name,
        "level": dbin.level,
        "office_id": dbin.office_id,
        "depth": dbin.depth,
        "location": loc(dbin.location),
        "level_status": dbin.level_status,
        "identifier": dbin.identifier
    } for dbin in dbins]

    return jsonify(result)

