from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/dashboard')
# @login_required
def dashboard():
    
    return render_template('user_dashboard.html')
