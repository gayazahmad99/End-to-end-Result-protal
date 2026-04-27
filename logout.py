from flask import redirect, make_response,Blueprint
from flask_jwt_extended import unset_jwt_cookies


def logout():
    response = make_response(redirect('/'))
    unset_jwt_cookies(response)   # ✅ CLEAR TOKEN
    return response