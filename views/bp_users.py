from flask import render_template, request, redirect, session, flash, url_for, Blueprint, current_app
from controllers.database_users_query import Controller as dbUQ
from controllers.database_users_auth import Controller as dbUA
from controllers.database_users_cd import Controller as dbUCD
from controllers.table_headers import Controller as tblCtrl


# ASSIGNMENTS
bp_users = Blueprint('bp_users', __name__)
db = current_app.extensions['sqlalchemy']


## USER ROUTES
# LOGIN
@bp_users.route('/login')
def login():
    from_pg = request.args.get('from')
    if not dbUA.user_auth_check():
        return render_template('/login.html')
    else:
        return redirect(url_for('views.index'))


# AUTH
@bp_users.route('/auth', methods=['POST',])
def auth():
    login = dbUA.user_auth(request, True)
    if login:
        goto_page = request.form['from_page']
        return redirect(f'/{goto_page}')
    else:
        return redirect(url_for('bp_users.login'))


# LOGOUT
@bp_users.route('/logout')
def logout():
    dbUA.user_auth_logoff()
    return redirect(url_for('bp_users.login'))


# LIST/CREATE USERS
@bp_users.route('/users', methods=['GET', 'POST',])
def users():
    if not dbUA.user_auth_check():
        return redirect(url_for('views.index', from_page=url_for('bp_users.users')))
    else:
        test = ""
        if request.method == 'POST':
            user_query = dbUQ.user_query_one(request.form['email'])
            if len(user_query) == 0:
                test = dbUCD.user_create(request)
            else:
                print('User already exists!')
        users_query = dbUQ.user_query_list()
        user_header_dict = tblCtrl.get_users_th()
        return render_template('users.html', logged=True, users_list=users_query, header_dict=user_header_dict, test_mail=test)


# USER DETAILS
@bp_users.route('/user_details', methods=['GET', ])
def user_details():
    if not dbUA.user_auth_check():
        return redirect(url_for('views.index', from_page=url_for('bp_users.user_details')))
    else:
        user_query = dbUQ.user_query_one(request.values.get('user_data'))
        user_header_dict = tblCtrl.get_users_th()
        return render_template('user_details.html', logged=True, user_list=user_query, header_dict=user_header_dict)


# UPDATE USERS
@bp_users.route('/user_details_update', methods=['POST', ])
def user_details_update():
    if not dbUA.user_auth_check():
        return redirect(url_for('views.index', from_page=url_for('bp_users.user_details')))
    else:
        if request.method == 'POST':
            dbUCD.user_update(request)
        return redirect(url_for('bp_users.users', from_page=url_for('bp_users.user_details')))


# DELETE USERS
@bp_users.route('/user_delete', methods=['GET', 'POST', ])
def user_delete():
    if not dbUA.user_auth_check():
        return redirect(url_for('views.index', from_page=url_for('bp_users.user_details')))
    else:
        dbUCD.user_delete(request)
        return redirect(url_for('bp_users.users', from_page=url_for('bp_users.user_details')))