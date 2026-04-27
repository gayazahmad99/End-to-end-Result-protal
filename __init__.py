from flask import Flask,redirect,flash,make_response
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret123"

    app.config["JWT_SECRET_KEY"] = "jwt-secret-key"

    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    jwt.init_app(app)

    # 🔥 TOKEN EXPIRED
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        response = make_response(redirect('/?expired=1'))
        response.set_cookie("access_token_cookie", "", expires=0)
        return response

    # 🔥 INVALID TOKEN
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return redirect('/?expired=1')


    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        flash("Session expired ❌ Please login again", "danger")
        return redirect('/')

    # ================= IMPORT FILES =================
    from app.routes.auth import login, logout, forget, exit
    from app.routes import register, dashboard, course, student, result, view_result

    # ================= REGISTER ROUTES =================
    app.add_url_rule('/', view_func=login.login, methods=['GET','POST'])
    app.add_url_rule('/logout', view_func=logout.logout)
    app.add_url_rule('/forget', view_func=forget.forget, methods=['GET','POST'])
    app.add_url_rule('/exit', view_func=exit.exit_app)

    app.add_url_rule('/register', view_func=register.register, methods=['GET','POST'])
    app.add_url_rule('/dashboard', view_func=dashboard.dashboard)

    app.add_url_rule('/course', view_func=course.course, methods=['GET','POST'])
    app.add_url_rule('/delete_course/<int:id>', view_func=course.delete_course, methods=['POST'])

    app.add_url_rule('/student', view_func=student.student, methods=['GET','POST'])
    app.add_url_rule('/update_student/<int:id>', view_func=student.update_student, methods=['POST'])
    app.add_url_rule('/delete_student/<int:id>', view_func=student.delete_student)

    app.add_url_rule('/result', view_func=result.result, methods=['GET','POST'])
    app.add_url_rule('/get_student/<int:student_id>', view_func=result.get_student)

    app.add_url_rule('/view_result', view_func=view_result.view_result, methods=['GET','POST'])

    return app


app = create_app()