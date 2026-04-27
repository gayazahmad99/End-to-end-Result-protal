from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import redirect, flash

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # ✅ check JWT exists
            verify_jwt_in_request()

            claims = get_jwt()
            role = claims.get("role")

            # ❌ no role found
            if not role:
                flash("Role missing in token ❌", "danger")
                return redirect('/dashboard')

            # ❌ not admin
            if role != "admin":
                flash("Admin access only ❌", "danger")
                return redirect('/dashboard')

            return fn(*args, **kwargs)

        except Exception:
            flash("Session expired or invalid token ❌", "danger")
            return redirect('/')

    return wrapper
    # wrapper.__name__ = fn.__name__
    # return wrapper