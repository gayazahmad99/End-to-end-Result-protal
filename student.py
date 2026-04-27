from flask import request, render_template, redirect, flash,Blueprint
from config import get_db_connection
from flask_jwt_extended import jwt_required
import psycopg2.extras


# ================= STUDENT =================

@jwt_required()
def student():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # ================== INSERT ==================
    if request.method == 'POST':
        data = request.form

        if not data.get('roll_no') or not data.get('name'):
            flash("Required fields missing ❌", "danger")
            return redirect('/student')

        if not data.get('gender'):
            flash("Select gender ❌", "danger")
            return redirect('/student')

        if not data.get('course_id'):
            flash("Select course ❌", "danger")
            return redirect('/student')

        try:
            cur.execute("""
            INSERT INTO students
            (roll_no, name, email, gender, dob, contact, course_id, state, city, pin, address, admission_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (data.get('roll_no'), data.get('name'), data.get('email'),
             data.get('gender'), data.get('dob'), data.get('contact'),
             data.get('course_id'), data.get('state'), data.get('city'),
             data.get('pin'), data.get('address'), data.get('admission_date')))

            conn.commit()
            flash("Student Added 👨‍🎓", "success")

        except Exception as e:
            conn.rollback()

            # PostgreSQL duplicate error fix
            if "duplicate key" in str(e).lower():
                flash("❌ Roll No already exists!", "danger")
            else:
                flash("❌ Something went wrong!", "danger")

        return redirect('/student')

    # ================== LOAD COURSES ==================
    cur.execute("SELECT id, name FROM courses")
    courses = cur.fetchall()

    # ================== 🔍 SEARCH ==================
    search = request.args.get('search')

    if search:
        cur.execute("""
            SELECT students.*, courses.name AS course_name
            FROM students
            LEFT JOIN courses ON students.course_id = courses.id
            WHERE students.roll_no ILIKE %s
        """, (f"%{search}%",))
    else:
        cur.execute("""
            SELECT students.*, courses.name AS course_name
            FROM students
            LEFT JOIN courses ON students.course_id = courses.id
        """)

    students = cur.fetchall()

    conn.close()

    return render_template('student.html', students=students, courses=courses)


# ================= UPDATE STUDENT =================
@jwt_required()
def update_student(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        UPDATE students
        SET roll_no=%s,
            name=%s,
            email=%s,
            gender=%s,
            dob=%s,
            contact=%s,
            course_id=%s,
            state=%s,
            city=%s,
            pin=%s,
            address=%s,
            admission_date=%s
        WHERE id = %s
    """,
    (request.form.get('roll_no'), request.form.get('name'), request.form.get('email'),
     request.form.get('gender'), request.form.get('dob'), request.form.get('contact'),
     request.form.get('course_id'), request.form.get('state'), request.form.get('city'),
     request.form.get('pin'), request.form.get('address'),
     request.form.get('admission_date'), id))

    conn.commit()
    conn.close()

    flash("Student Updated ✏️", "info")
    return redirect('/student')


# ================= DELETE STUDENT =================
@jwt_required()#
def delete_student(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    flash("Student Deleted 🗑", "info")
    return redirect('/student')