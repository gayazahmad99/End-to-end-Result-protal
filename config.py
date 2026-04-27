import os
import psycopg2

def get_db_connection():
    if os.getenv("DATABASE_URL"):
        db_url = os.getenv("DATABASE_URL")

        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://")

        return psycopg2.connect(db_url)

    # LOCAL fallback
    return psycopg2.connect(
        host="localhost",
        database="student_result_system",
        user="postgres",
        password="root123"
    )