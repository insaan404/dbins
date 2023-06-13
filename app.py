import os
import json
import pathlib

import flask
from flask import send_from_directory, Response, Flask, request, session, redirect, render_template, jsonify,flash
from flask_cors import CORS

import requests as reqs
import requests
from dotenv import load_dotenv


from src.api.routes import api
from src.models.adminstration import Role
import src.use_cases.vehicle
from src.web_routes.administration import adminst_bp
import src.use_cases.administration as uc_admin
import src.use_cases.office as uc_office

from src.events.event_store import EventStore, socketio

from src.web_routes.caches import user_cache_repo, UserCache
from src.common.auth_utils import create_token, decode_token

API_TOKENS = {}


load_dotenv()
app = Flask(__name__)
socketio.init_app(app)
app.secret_key = os.getenv("key")
app.register_blueprint(adminst_bp, url_prefix="/administration")
app.register_blueprint(api, url_prefix="/api")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})



BDir = pathlib.Path(__file__).parent
URL = "http://localhost:8080"


@app.get("/media/static/images")
def __get_static_images():
    img = request.args.get("image")
    pth = str(BDir) + "\\static\\images\\"
    return send_from_directory(pth, img)


def _login():
    form = request.form
    username = form.get("username")
    password = form.get("password")

    user = uc_admin.get_user_by_username(username)
    if not user or user.password != password:
        flash("wrong credentials")
        return redirect(f"/")
    session["token"] = create_token(user)

    # resp = reqs.post(f"{URL}/api/login",
                # data=json.dumps({"username": user.username, "password": user.password, "device": "webapp"}),
                # headers={"Content-Type": "Application/json"})

    token = session.get("token")
    cache = UserCache(token)
    user_cache_repo.add_cache(user.id, cache)
    return redirect("/")


def _user_home(user):
    office = uc_admin.get_user_office(user)
    cache = user_cache_repo.get_cache(user.id)
    if not cache:
        session["token"] = ''
        return redirect("/")
    token = cache.get_api_token()
    return render_template("user/user_home.html", office=office, user=user, token=token)


def _root_home(user):
    offices = uc_office.get_all_offices(user)
    cache = user_cache_repo.get_cache(user.id)
    print("office: ", offices)
    if not cache:
        session["token"] = ''
        return redirect("/")
    api_token = cache.get_api_token()
    
    return render_template("root/root_home.html", offices=offices, api_token=api_token)


def _home():
    token = session.get("token")
    if not token:
        return render_template("login.html")
    user = decode_token(token)
    if user.role == Role.ROOT:
        return _root_home(user)
    return _user_home(user)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return _login()
    else:
        return _home()
    


@app.get("/logout")
def _logout():
    session["token"] = ''
    return redirect("/")




@app.get("/api/token")
def _get_token():
    return jsonify({"token": session.get("token")})




if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080, host='0.0.0.0')





