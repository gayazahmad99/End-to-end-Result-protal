from flask import request, redirect, render_template, flash, make_response,Blueprint
from flask_jwt_extended import create_access_token, set_access_cookies
from werkzeug.security import check_password_hash
from config import get_db_connection


def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT password, role FROM users WHERE email=%s", (email,))
        user = cur.fetchone()


        cur.close()
        conn.close()

        # ✅ BONUS FIX 1: user exist check
        if not user:
            flash("User not found ❌", "danger")
            return render_template('login.html')

        # ✅ password check
        if check_password_hash(user[0], password):

            # ✅ JWT TOKEN (correct role placement)
            token = create_access_token(
                identity=email,
                additional_claims={
                    "role": user[1]
                }
            )
            # ✅ JWT ADDED (IMPORTANT FIX)
            response = make_response(redirect('/dashboard'))
            set_access_cookies(response, token)

            flash("Login Successful ✅", "success")
            return response

        else:
            flash("Invalid Email or Password ❌", "danger")

    return render_template('login.html')