from flask import request, render_template, redirect, flash,Blueprint
from config import get_db_connection
from flask_jwt_extended import jwt_required
import psycopg2.extras


# ================= COURSE =================

@jwt_required()
def course():

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    search_query = request.args.get('search')

    # ================= INSERT / UPDATE =================
    if request.method == 'POST':
        name = request.form.get('name')
        duration = request.form.get('duration')
        charges = request.form.get('charges')
        description = request.form.get('description')
        course_id = request.form.get('id')

        if not name:
            flash("Course name required ❌", "danger")
            return redirect('/course')

        try:
            # ================= UPDATE =================
            if course_id and course_id.isdigit():
                cur.execute("""
                    UPDATE courses 
                    SET name=%s, duration=%s, charges=%s, description=%s 
                    WHERE id=%s
                """, (name, duration, charges, description, course_id))

                flash("Course Updated ✏️", "info")

            # ================= INSERT =================
            else:
                cur.execute("""
                    INSERT INTO courses(name, duration, charges, description)
                    VALUES(%s, %s, %s, %s)
                """, (name, duration, charges, description))

                flash("Course Added 📚", "success")

            conn.commit()

        except Exception as e:
            conn.rollback()


            # PostgreSQL specific error handling

            if "duplicate key" in str(e).lower():
                flash("Course already exists ❌", "danger")
            else:
                flash(f"Error: {str(e)}", "danger")

        return redirect('/course')

    # ================= SEARCH =================
    if search_query:
        cur.execute("""
            SELECT * FROM courses 
            WHERE name ILIKE %s
        """, ('%' + search_query + '%',))
    else:
        cur.execute("SELECT * FROM courses")

    data = cur.fetchall()


    conn.close()

    return render_template('course.html', courses=data)


# ================= DELETE COURSE =================
@jwt_required()
def delete_course(id):

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cur.execute("DELETE FROM courses WHERE id=%s", (id,))
        conn.commit()
        flash("Course Deleted 🗑️", "danger")

    except Exception as e:
        conn.rollback()
        flash(f"Error: {str(e)}", "danger")

    conn.close()

    return redirect('/course')