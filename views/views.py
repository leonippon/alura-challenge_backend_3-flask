from flask import render_template, request, redirect, session, url_for, Blueprint, current_app
from controllers.database_users_auth import Controller as dbUA


# ASSIGNMENTS
views = Blueprint('views', __name__)
db = current_app.extensions['sqlalchemy']


## ROUTES
# ROOT / INDEX
@views.route('/')
def index():
    if not dbUA.user_auth_check():
        return redirect(url_for('bp_users.login'))
    else:
        return render_template('index.html', logged=True)