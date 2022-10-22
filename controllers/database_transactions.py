from flask import current_app
import db.models as models


# Catch DB
db = current_app.extensions['sqlalchemy']


class Controller:
    @staticmethod
    def transaction_insert(transaction):
        db.session.add(transaction)
        db.session.commit()


    @staticmethod
    def transaction_list_upload(transaction_list):
        for transaction in transaction_list:
            Controller.transaction_insert(transaction)


    @staticmethod
    def transaction_query_imported():
        result = db.session.execute(db.select(models.Transaction).group_by(models.Transaction.transaction_date).order_by(models.Transaction.transaction_date)).all()
        if len(result) > 0:
            print('Some entry found!')
            return result
        else:
            print('No entry found')
            return [[]]


    @staticmethod
    def transaction_query_detailed(req_transaction_date, is_validation):
        result = db.session.execute(db.select(models.Transaction).filter_by(transaction_date=req_transaction_date).order_by(models.Transaction.transaction_date)).all()
        if len(result) > 0:
            if is_validation:
                print('Validation #4 Error, upload already exists!')
                return False
            else:
                print('Some entry found!')
                return result
        else:
            if is_validation:
                print('Validation #4 Ok!')
                return True
            else:
                print('No entry found')
                return [[]]


    @staticmethod
    def transaction_query_reports(req_upload_date):
        result = db.session.execute(db.select(models.Transaction).filter_by(upload_date=req_upload_date).order_by(models.Transaction.transaction_date)).all()
        if len(result) > 0:
            print('Some entry found!')
            return result
        else:
            print('No entry found')
            return [[]]