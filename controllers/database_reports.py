from flask import current_app
import db.models as models
import os


# Catch DB
db = current_app.extensions['sqlalchemy']


class Controller:
    @staticmethod
    def get_suspicious_transactions(req_transaction_date):
        # ROLLBACK
        db.session.rollback()
        # QUERY
        result = db.session.execute((db.select(models.Transaction)\
                                    .where(models.Transaction.transaction_value > 100000))\
                                    .filter_by(transaction_date=req_transaction_date)).all()
        if len(result) > 0:
            return result
        else:
            print('No suspicious transaction found in this date!')
            return []


    @staticmethod
    def get_suspicious_accounts(req_transaction_date):
        # ROLLBACK
        db.session.rollback()
        # OUTGOING
        result_out = db.session.execute(db.select(models.Transaction.origin_bank, models.Transaction.origin_agency, models.Transaction.origin_account, models.Transaction.transaction_date, db.func.sum(models.Transaction.transaction_value).label('transactions_total'))\
                                        .where(db.extract('year', models.Transaction.transaction_date) == req_transaction_date[:4])\
                                        .where(db.extract('month', models.Transaction.transaction_date) == req_transaction_date[5:7])\
                                        .group_by(models.Transaction.origin_bank, models.Transaction.origin_agency, models.Transaction.origin_account, models.Transaction.transaction_date)\
                                        .having(db.text(f'transactions_total >= {current_app.config.get("LIMIT_ACC")}'))\
                                        ).all()
        # INCOMING
        result_in = db.session.execute(db.select(models.Transaction.destination_bank, models.Transaction.destination_agency, models.Transaction.destination_account, models.Transaction.transaction_date, db.func.sum(models.Transaction.transaction_value).label('transactions_total'))\
                                        .where(db.extract('year', models.Transaction.transaction_date) == req_transaction_date[:4])\
                                        .where(db.extract('month', models.Transaction.transaction_date) == req_transaction_date[5:7])\
                                        .group_by(models.Transaction.destination_bank, models.Transaction.destination_agency, models.Transaction.destination_account, models.Transaction.transaction_date)\
                                        .having(db.text(f'transactions_total >= {current_app.config.get("LIMIT_ACC")}'))\
                                        ).all()
        if len(result_out) > 0 and len(result_in) > 0:
            return [result_out, result_in]
        elif len(result_out) > 0 or len(result_in) > 0:
            print('Query error, only one result is found')
        else:
            print('No suspicious account found in this date!')
            return [], []


    @staticmethod
    def get_suspicious_agencies(req_transaction_date):
        # ROLLBACK
        db.session.rollback()
        # OUTGOING
        result_out = db.session.execute(db.select(models.Transaction.origin_bank, models.Transaction.origin_agency, models.Transaction.transaction_date, db.func.sum(models.Transaction.transaction_value).label('transactions_total'))\
                                        .where(db.extract('year', models.Transaction.transaction_date) == req_transaction_date[:4])\
                                        .where(db.extract('month', models.Transaction.transaction_date) == req_transaction_date[5:7])\
                                        .group_by(models.Transaction.origin_bank, models.Transaction.origin_agency, models.Transaction.transaction_date)\
                                        .having(db.text(f'transactions_total >= {current_app.config.get("LIMIT_AG")}'))\
                                        ).all()
        # INCOMING
        result_in = db.session.execute(db.select(models.Transaction.destination_bank, models.Transaction.destination_agency, models.Transaction.transaction_date, db.func.sum(models.Transaction.transaction_value).label('transactions_total'))\
                                        .where(db.extract('year', models.Transaction.transaction_date) == req_transaction_date[:4])\
                                        .where(db.extract('month', models.Transaction.transaction_date) == req_transaction_date[5:7])\
                                        .group_by(models.Transaction.destination_bank, models.Transaction.destination_agency, models.Transaction.transaction_date)\
                                        .having(db.text(f'transactions_total >= {current_app.config.get("LIMIT_AG")}'))\
                                        ).all()
        if len(result_out) > 0 and len(result_in) > 0:
            return [result_out, result_in]
        elif len(result_out) > 0 or len(result_in) > 0:
            print('Query error, only one result is found')
        else:
            print('No suspicious agency found in this date!')
            return [], []
