import uuid
import re
import json

from flask import session, render_template, request, redirect, Blueprint, make_response, flash
import requests as reqs

from src.models.adminstration import Role
from src.models.geometries import Boundry, Coordinates
import src.models.requests_responses as rp
from src.web_auth import web_auth
import src.use_cases.office as uc_office
import src.use_cases.administration as uc_admin
import src.use_cases.drivers as uc_drivers
import src.use_cases.wda as uc_wda
import src.use_cases.vehicle as uc_vehicle
import src.use_cases.dbin as uc_dbins
from src.web_routes.caches import user_cache_repo

adminst_bp = Blueprint("root administration", __name__)


def _root_administration(user):
    return redirect("/administration/offices")



@adminst_bp.route("/", methods=["GET"])
@web_auth
def administration(user):
    if user.role == Role.ROOT:
        return _root_administration(user)
    else:
        return "<h1>not authorized<h1>"


@adminst_bp.route("/drivers/", methods=["GET"])
@web_auth
def _drivers(user):
    offices = uc_office.get_all_offices(user)
    return render_template("root/root_administration_drivers.html", offices=offices)


@adminst_bp.route("/drivers/all")
@web_auth
def _get_drivers(user):
    office_id = request.args.get("office")
    if not office_id:
        drivers = uc_drivers.all_drivers(user)
        return render_template("partials/root_drivers.html", drivers=drivers)
    else:
        drivers = uc_drivers.get_office_drivers(user, office_id)
        return render_template("partials/root_drivers.html", drivers=drivers)


@adminst_bp.route("/drivers/add", methods=["GET"])
@web_auth
def _add_driver_get(user):
    offices = uc_office.get_all_offices(user)
    vehicles = uc_vehicle.get_all_vehicles(user)
    return render_template("partials/add_driver.html", offices=offices, vehicles=vehicles)


@adminst_bp.route("/drivers/add", methods=["POST"])
@web_auth
def _add_driver_post(user):
    form = request.form
    req = rp.CreateDriverReq(
        fname=form.get("fname"),
        lname=form.get("lname"),
        address=form.get("address"),
        contact=form.get("contact"),
        office_id=uuid.UUID(form.get("office")),
        vehicle_id=uuid.UUID(form.get("vehicle")),
        username=form.get("username"),
        password=form.get("password")
    )
    
    result = uc_admin.add_driver(user, req)

    resp = make_response(render_template("partials/add_driver.html"))
    resp.headers["HX-Trigger"] = "saved"
    resp.headers["HX-Redirect"] = "/administration/drivers/"
    return resp



@adminst_bp.route("/offices", methods=["GET"])
@web_auth
def _offices(_):
    return render_template("root/root_administration_office.html")


@adminst_bp.route("/offices/all")
@web_auth
def _offices_all(user):
    offices = uc_office.get_all_offices(user)
    return render_template("partials/root_office_all.html", offices=offices)


def _decode_coordinate(string) -> Coordinates|None:
    pattern = r'{"lat":(\d+\.\d+),"lng":(\d+\.\d+)}'
    match = re.search(pattern, string)
    crd = None
    if match:
        print("match")
        lat = float(match.group(1))
        lng = float(match.group(2))
        crd = Coordinates(lat, lng)
    return crd


def _add_office_post(user):
    pattern = r'{"lat":\d+\.\d+,"lng":\d+\.\d+}'
    matches = re.findall(pattern, request.form.get("coordinates"))
    coords_str = "[" + ", ".join(matches) + "]"
    coords = json.loads(coords_str)
    area_name = request.form.get("area_name")
    wda = uuid.UUID(request.form.get("wda"))
    bd_area = Boundry(
            [Coordinates(crd['lat'], crd['lng']) for crd in coords]
        )
    terminal_location = _decode_coordinate(request.form.get("vehicle_terminal"))
    req = rp.AddOfficeReq(area_name, wda, bd_area, terminal_location)
    office = uc_admin.add_office(user, req)
    if office:
        resp = make_response(render_template("partials/root_office_add.html"))
        resp.headers["HX-Trigger"] = "saved"
        resp.headers["HX-Redirect"] = "/administration"
        return resp
    else:
        wdas = uc_wda.get_all(user)
        return render_template("partials/root_office_add.html", wdas=wdas)


@adminst_bp.route("/offices/add", methods=["GET", "POST"])
@web_auth
def _add_office(user):
    cache = user_cache_repo.get_cache(user.id)
    if request.method == "POST":
        return _add_office_post(user)
    else:
        wdas = uc_wda.get_all(user)
        token = cache.get_api_token()
        return render_template("partials/root_office_add.html", api_token=token, wdas=wdas)



@adminst_bp.route("/users", methods=["GET"])
def _users():
    return render_template("roo/root_administration_users.html")


@adminst_bp.get("/dbins")
@web_auth
def _root_dbins(user):
    offices = uc_office.get_all_offices(user)
    return render_template("root/root_administration_dbins.html", offices=offices)


def _add_level_pcnt(dbins):
    levels = {}
    for dbin in dbins:
        level = dbin.level
        pcnt = 0
        if level != 0:
            pcnt = int((dbin['level']/dbin['dimensions']['volume'])*100)
        levels[dbin.id.hex] = pcnt
    return levels


@adminst_bp.get("/dbins/all")
@web_auth
def _dbins_all_get(user):
    office_id = request.args.get("office")
    if office_id:
        return office_dbins(user, uuid.UUID(office_id))
    dbins = uc_dbins.get_all_dustbins(user)
    levels = _add_level_pcnt(dbins)
    return render_template("partials/root_dbins_all.html", dbins=dbins, levels=levels)


def office_dbins(user, id):
    dbins = list(uc_dbins.get_office_dbins(user, id))
    levels = _add_level_pcnt(dbins)
    return render_template("partials/root_dbins_all.html", dbins=dbins, levels=levels)


@adminst_bp.get("/dbins/add")
@web_auth
def _dbin_add_get(user):
    offices = uc_office.get_all_offices(user)
    cache = user_cache_repo.get_cache(user.id)
    if not cache:
        session["token"] = ''
        return redirect("/")
    return render_template("partials/add_dbin.html", offices=offices, api_token=cache.get_api_token())


@adminst_bp.post("/dbins/add")
@web_auth
def _dbin_add_post(user):
    form = request.form
    pattern = r'{"lat":(\d+\.\d+),"lng":(\d+\.\d+)}'
    match = re.search(pattern, form.get("location"))
    crd = None
    if match:
        print("match")
        lat = float(match.group(1))
        lng = float(match.group(2))
        crd = Coordinates(lat, lng)

    req = rp.InstallDBinReq(form.get("name"), form.get("identifier"), uuid.UUID(form.get("office")),
                            crd, float(form.get("depth")))
    uc_dbins.install_dustbin(user, req)
    resp = make_response(render_template("partials/add_dbin.html"))
    resp.headers["HX-Trigger"] = "saved"
    resp.headers["HX-Redirect"] = "/administration/dbins"
    return resp
    

@adminst_bp.get("/vehicles")
@web_auth
def _get_vehicles(user):
    offices = uc_office.get_all_offices(user)
    return render_template("root/root_administration_vehicles.html", offices=offices)


@adminst_bp.get("/vehicles/all")
@web_auth
def _get_vehicles_all(user):
    vehicles = uc_vehicle.get_all_vehicles(user)
    return render_template("partials/root_vehicles_all.html", vehicles=vehicles)


@adminst_bp.get("/vehicles/add")
@web_auth
def _vehicle_add_get(user):
    offices = uc_office.get_all_offices(user)
    return render_template("partials/add_vehicle.html", offices=offices)
    

@adminst_bp.post("/vehicles/add")
@web_auth
def _vehicle_add_post(user):
    form = request.form
    office_id = form.get("office")
    if office_id:
        office_id = uuid.UUID(office_id)
    else:
        office_id = None
    req = rp.AddVehicleReq(form.get("plate_no"), office_id)
    vehicle = uc_admin.add_vehicle(user, req)
    if vehicle:
        resp = make_response(render_template("partials/root_office_add.html"))
        resp.headers["HX-Trigger"] = "saved"
        resp.headers["HX-Redirect"] = "/administration/vehicles"
        return resp

    flash("something went wrong")
    return redirect("/vehicles/add")


@adminst_bp.get("/wdas")
@web_auth
def _get_wdas(user):
    return render_template("root/root_administration_wda.html")


@adminst_bp.get("/wdas/all")
@web_auth
def _get_wdas_all(user):
    wdas = uc_wda.get_all(user)
    return render_template("partials/wda_all.html", wdas=wdas)


@adminst_bp.get("/wdas/add")
@web_auth
def _get_wda_add(user):
    return render_template("partials/add_wda.html")
    

@adminst_bp.post("/wdas/add")
@web_auth
def _add_wda_post(user):
    form = request.form
    pattern = r'{"lat":"(\d+\.\d+)","lng":"(\d+\.\d+)"}'
    match = re.search(pattern, form.get("location"))
    crd = None
    if match:
        lat = float(match.group(1))
        lng = float(match.group(2))
        crd = Coordinates(lat, lng)

    req = rp.AddWDAReq(form.get("name"), crd, int(form.get("area")))
    uc_wda.add_wda(user, req)
    resp = make_response(render_template("partials/add_wda.html"))
    resp.headers["HX-Trigger"] = "saved"
    resp.headers["HX-Redirect"] = "/administration/wdas"
    return resp
















