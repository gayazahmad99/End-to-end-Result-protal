from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash

# =========================
# 👤 USERS TABLE
# =========================
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    contact = db.Column(db.String(20))

    email = db.Column(db.String(100), unique=True)

    security_question = db.Column(db.Text)
    answer = db.Column(db.Text)

    password = db.Column(db.String(255))
    confirm_password = db.Column(db.Text)

    terms = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

# =========================
# 📚 COURSES TABLE
# =========================
class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    duration = db.Column(db.String(50))
    charges = db.Column(db.Numeric)
    description = db.Column(db.Text)

    # relation with students
    students = db.relationship('Student', backref='course', lazy=True)

    def __repr__(self):
        return f"<Course {self.name}>"

# =========================
# 👨‍🎓 STUDENTS TABLE
# =========================
class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)

    roll_no = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    gender = db.Column(db.String(10))

    dob = db.Column(db.Date)

    contact = db.Column(db.String(20))

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)

    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    pin = db.Column(db.String(10))
    address = db.Column(db.Text)

    admission_date = db.Column(db.Date, default=datetime.utcnow)
    # relation with results
    results = db.relationship('Result', backref='student', lazy=True)

    def __repr__(self):
        return f"<Student {self.name}>"

# =========================
# 📊 RESULTS TABLE
# =========================
class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)

    name = db.Column(db.String(100))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    obtained_marks = db.Column(db.Integer)
    total_marks = db.Column(db.Integer)

    percentage = db.Column(db.Float)

    def __repr__(self):
        return f"<Result {self.name} {self.percentage}%>"