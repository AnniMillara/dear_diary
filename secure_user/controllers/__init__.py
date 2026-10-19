from functools import wraps
from flask import flash, redirect, session, url_for


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("usuario_id"):
            flash("Debes iniciar sesión para continuar.", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped
