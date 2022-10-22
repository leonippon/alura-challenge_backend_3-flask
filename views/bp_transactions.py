from flask import render_template, request, redirect, session, url_for, Blueprint, current_app
from controllers.database_transactions import Controller as dbTctrl
from controllers.database_users_auth import Controller as dbUA
from controllers.database_reports import Controller as dbR
from controllers.table_headers import Controller as tblCtrl
from controllers.transactions import Controller as trCtrl
from controllers.importer import Controller as impCtrl


# ASSIGNMENTS
bp_transactions = Blueprint('bp_transactions', __name__)
db = current_app.extensions['sqlalchemy']


## TRANSACTION ROUTES
# IMPORT FILE / IMPORTED
@bp_transactions.route('/imports', methods=['GET', 'POST'])
def imports():
    if not dbUA.user_auth_check():
        return redirect(url_for('bp_users.login', from_page=url_for('bp_transactions.imports')))
    else:
        if request.method == 'POST':
            impCtrl.run_importer(request)
        transaction_query = trCtrl.change_tf_format(dbTctrl.transaction_query_imported())
        table_header = tblCtrl.get_imported_th()
        return render_template('imports.html', logged=True, header_dict=table_header, transaction_list=transaction_query)


# DETAILS
@bp_transactions.route('/details', methods=['POST'])
def details():
    if not dbUA.user_auth_check():
        return redirect(url_for('bp_users.login', from_page=url_for('bp_transactions.details')))
    else:
        if request.method == 'POST':
            table_header = tblCtrl.get_transaction_th()
            transaction_query = trCtrl.change_tf_format(trCtrl.unpack_transactions(dbTctrl.transaction_query_detailed(request.values.get('tr_date'), False), 1))
            table_u_header = tblCtrl.get_uploader_th()
            table_u_query = trCtrl.change_tf_format(trCtrl.unpack_transactions(dbTctrl.transaction_query_detailed(request.values.get('tr_date'), False), 2))
        else:
            transaction_query = [[]]
            table_header = [[]]
            table_u_header = [[]]
            table_u_query = [[]]
        return render_template('details.html', logged=True, header_u_dict=table_u_header, user_list=table_u_query, header_dict=table_header, transaction_list=transaction_query)


# REPORTS
@bp_transactions.route('/reports', methods=['GET', 'POST'])
def reports():
    if not dbUA.user_auth_check():
        return redirect(url_for('bp_users.login', from_page=url_for('reports')))
    else:
        # GET HEADERS
        table_tr_header = tblCtrl.get_sus_tr_th()
        table_acc_header = tblCtrl.get_sus_acc_th()
        table_ag_header = tblCtrl.get_sus_ag_th()
        # QUERY DATES
        transaction_query = dbTctrl.transaction_query_imported()
        date_query = tblCtrl.get_date_tables(transaction_query)
        # GET REPORT
        if request.method == 'POST' and (request.form['Transações'] is not None or request.form['Transações'] != ""):
            transaction_query_1 = trCtrl.change_tf_format(trCtrl.unpack_transactions(dbR.get_suspicious_transactions(request.form['Transações']), 0))
            transaction_query_2 = trCtrl.change_tf_format(trCtrl.reorder_data(dbR.get_suspicious_accounts(request.form['Transações'])))
            transaction_query_3 = trCtrl.change_tf_format(trCtrl.reorder_data(dbR.get_suspicious_agencies(request.form['Transações'])))
        else:
            # GET EMPTY
            transaction_query_1 = []
            transaction_query_2 = []
            transaction_query_3 = []
        return render_template('reports.html', logged=True, date_list=date_query, header_dict_1=table_tr_header, header_dict_2=table_acc_header,
                                header_dict_3=table_ag_header, transaction_list_1=transaction_query_1, transaction_list_2=transaction_query_2,
                                transaction_list_3=transaction_query_3)