from flask import current_app
from flask import session
import db.models as models


# Catch DB
db = current_app.extensions['sqlalchemy']


class Controller:
    @staticmethod
    def user_list_remove_admin(user_list):
        for user in user_list:
            # Pop ADMIN or ITSELF
            if user[0].email == "admin@email.com.br" or user[0].email == session['user_logged']:
                user_list.pop(user_list.index(user))
        return user_list


    @staticmethod
    def user_query_all():
        n_result = db.session.execute(db.select(models.User).filter_by(active="1")).all()
        result = n_result[0]
        if len(result) > 0:
            print('Some entry found!')
            return result
        else:
            print('No entry found')
            return [[]]


    @staticmethod
    def user_query_list():
        # Query
        nn_result = db.session.execute(db.select(models.User).filter_by(active=1)).all()
        # Validate Query
        result = Controller.user_list_remove_admin(nn_result)
        if result is not None or result != "":
            print('Some entry found!')
            return result
        else:
            print('No entry found')
            return [[]]


    @staticmethod
    def user_query_one(request):
        # Query
        result = db.session.execute(db.select(models.User).filter_by(email=request, active=1)).all()
        # Validate Query
        if len(result) > 0:
            user = result[0][0]
        else:
            user = result
        if user is not None or user != "":
            print('Some entry found!')
            return result
        else:
            print('No entry found')
            return [[]]