from flask import request, redirect, render_template, flash,Blueprint
from werkzeug.security import generate_password_hash
from config import get_db_connection

# forget_bp = Blueprint('forget', __name__)
#
# @forget_bp.route('/forget', methods=['GET','POST'])
def forget():
    if request.method == 'POST':
        data = request.form

        hashed = generate_password_hash(data['new_password'])

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM users 
            WHERE email=%s AND answer=%s
        """, (data['email'], data['answer']))

        user = cur.fetchone()

        if user:
            cur.execute("UPDATE users SET password=%s WHERE email=%s",
                        (hashed, data['email']))
            conn.commit()
            flash("Password Updated 🔐", "success")
            return redirect('/')
        else:
            flash("Wrong Answer ❌", "danger")

    return render_template('forget.html')