from flask import render_template,Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity
from config import get_db_connection


@jwt_required()
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM students")
    students = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM courses")
    courses = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM results")
    results = cur.fetchone()[0]

    conn.close()

    return render_template("dashboard.html",
                           total_students=students,
                           total_courses=courses,
                           total_results=results)