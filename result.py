from flask import request, render_template, redirect, flash,Blueprint
from config import get_db_connection
from flask_jwt_extended import jwt_required


# ================= RESULT =================

@jwt_required()
def result():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':

        # ✅ SAFE GET (no crash)
        student_id = request.form.get('student_id')
        obtained = request.form.get('obtained_marks')
        total = request.form.get('total_marks')

        # ✅ VALIDATION
        if not student_id or not obtained or not total:
            flash("All fields required ❌", "danger")
            return redirect('/result')

        obtained = int(obtained)
        total = int(total)

        # ✅ avoid divide by zero
        if total == 0:
            flash("Total marks cannot be 0 ❌", "danger")
            return redirect('/result')

        percentage = (obtained / total) * 100

        # ✅ GET student name + course
        cur.execute("""
        SELECT students.id, students.roll_no, students.name, courses.name
        FROM students
        LEFT JOIN courses ON students.course_id = courses.id
        WHERE students.id=%s
        """, (student_id,))

        data = cur.fetchone()

        # ✅ SAFETY FIX
        if not data:
            flash("Student not found ❌", "danger")
            return redirect('/result')

        # ⚠️ IMPORTANT FIX (correct indexing)
        name = data[2]     # students.name
        course = data[3]   # courses.name

        # ✅ INSERT
        cur.execute("""
        INSERT INTO results(student_id,name,course,obtained_marks,total_marks,percentage)
        VALUES(%s,%s,%s,%s,%s,%s)
        """, (student_id, name, course, obtained, total, percentage))

        conn.commit()

        flash("Result Saved 📊", "success")
        return redirect('/result')

    # ✅ LOAD STUDENTS
    cur.execute("""
        SELECT students.id, students.roll_no, students.name, courses.name
        FROM students
        LEFT JOIN courses ON students.course_id = courses.id
    """)
    students = cur.fetchall()

    conn.close()

    return render_template('result.html', students=students)


# ================= GET STUDENT =================
@jwt_required()
def get_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT students.name, courses.name 
        FROM students
        LEFT JOIN courses ON students.course_id = courses.id
        WHERE students.id = %s
    """, (student_id,))

    data = cur.fetchone()
    conn.close()

    if data:
        return {
            "name": data[0],
            "course": data[1]
        }
    else:
        return {}