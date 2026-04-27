from flask import request, redirect, render_template, flash, Blueprint
from werkzeug.security import generate_password_hash
from config import get_db_connection


def register():
    if request.method == 'POST':
        data = request.form

        # ✅ SAFE ACCESS (no functionality change)
        password = data.get('password')

        if not password:
            flash("Password is required ❌", "danger")
            return redirect('/register')

        hashed = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email=%s", (data['email'],))
        if cur.fetchone():
            flash("Email exists ❌", "danger")
            return redirect('/register')

        cur.execute("""
        INSERT INTO users(first_name,last_name,contact,email,security_question,answer,password,role)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            data['first_name'], data['last_name'], data['contact'],
            data['email'], data['security_question'], data['answer'],
            hashed, 'student'
        ))

        conn.commit()
        conn.close()

        flash("Registered ✅", "success")
        return redirect('/')

    return render_template('register.html')