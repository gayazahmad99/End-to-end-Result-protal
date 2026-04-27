from flask import request, render_template,Blueprint
from config import get_db_connection
from flask_jwt_extended import jwt_required


# ================= VIEW RESULT =================

@jwt_required()
def view_result():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        roll = request.form.get('roll')

        # ✅ safety check (no crash if empty)
        if not roll:
            cur.execute("""
                SELECT students.roll_no, students.name, courses.name,
                       results.obtained_marks, results.total_marks, results.percentage
                FROM results
                JOIN students ON results.student_id = students.id
                LEFT JOIN courses ON students.course_id = courses.id
            """)
        else:
            cur.execute("""
                SELECT students.roll_no, students.name, courses.name,
                       results.obtained_marks, results.total_marks, results.percentage
                FROM results
                JOIN students ON results.student_id = students.id
                LEFT JOIN courses ON students.course_id = courses.id
                WHERE students.roll_no=%s
            """, (roll,))
    else:
        cur.execute("""
            SELECT students.roll_no, students.name, courses.name,
                   results.obtained_marks, results.total_marks, results.percentage
            FROM results
            JOIN students ON results.student_id = students.id
            LEFT JOIN courses ON students.course_id = courses.id
        """)

    data = cur.fetchall()
    conn.close()

    return render_template('view_result.html', results=data)