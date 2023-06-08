import functools

from flask import request, jsonify, Response

import src.use_cases.administration as uc_admin
from src.common.auth_utils import decode_token


def auth(f):
    @functools.wraps(f)
    def decorated(*args, **kw):
        token = request.headers.get("Authorization")
        print("full: ", token)
        if token:
            token = token[7:]
        else:
            return jsonify({"msg": "please login"})
        user = decode_token(token)
        if not user:
            return Response("auth failed", 401, content_type="Application/json") 
        return f(user, *args, **kw)

    return decorated




