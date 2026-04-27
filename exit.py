from flask import redirect, flash,Blueprint

# exit_bp = Blueprint('exit', __name__)
# @exit_bp.route('/exit', methods=['GET','POST'])
def exit_app():
    flash("Application Closed ❌", "info")
    return redirect('/')