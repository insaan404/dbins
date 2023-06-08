import functools

from flask import session, redirect

from .common.auth_utils import decode_token
from src.web_routes.caches import user_cache_repo


def web_auth(f):
    @functools.wraps(f)
    def _wrapper(*args, **kw):
        token = session.get("token")
        user = decode_token(token)
        if user:
            return f(user, *args, **kw)
        return redirect("/")
    
    return _wrapper








