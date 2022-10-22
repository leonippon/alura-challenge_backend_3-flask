from controllers.database_users_auth import Controller as dbUA
from controllers.mail import Controller as mailCtrl
from flask import current_app, request, session, flash
import db.models as models
import random
import bcrypt


# Catch DB & Mail
db = current_app.extensions['sqlalchemy']


class Controller:
    @staticmethod
    def hash_passwd(passwd):
        if passwd is not None and passwd != "":
            bytestream = passwd.encode('utf-8')
            salt_rounds = current_app.config['HASH_SALT_ROUNDS']
            salt = bcrypt.gensalt(salt_rounds)
            hash = bcrypt.hashpw(bytestream, salt)
            return hash, bytestream
        else:
            return ""


    @staticmethod
    def random_passwd():
        passwd = random.randint(100000, 999999)
        return passwd


    @staticmethod
    def user_create(req_user):
        # Check user type
        if type(req_user) == models.User:
            # Generate random password if not provided
            if req_user.password == None:
                passwd = str(Controller.random_passwd())
            else:
                passwd = req_user.password
            # Hash password
            hash, _ = Controller.hash_passwd(passwd)
            # Check empty fields
            if req_user.username is None or req_user.email is None:
                return print('Error, empty fields!')
            elif req_user.username == "" or req_user.email == "":
                return print('Error, empty fields!')
            else:
                # Create user model
                new_user = models.User(
                    username = req_user.username,
                    email = req_user.email,
                    password = hash
                    )
        else:
            # Generate random password if not provided
            passwd = str(Controller.random_passwd())
            # Hash password
            hash, _ = Controller.hash_passwd(passwd)
            # Create user model
            if req_user.form['username'] is None or req_user.form['email'] is None:
                return print('Error, empty fields!')
            elif req_user.form['username'] == "" or req_user.form['email'] == "":
                return print('Error, empty fields!')
            else:
                new_user = models.User(
                    username = req_user.form['username'],
                    email = req_user.form['email'],
                    password = hash
                    )
        try:
            # Insert on DB
            db.session.add(new_user)
            db.session.commit()
            #  Send Mail
            test = mailCtrl.send_pwd(new_user, passwd)
            return test
        except Exception:
            db.session.rollback()
            return print('Erro, não foi possível adicionar usuário!'), ""



    @staticmethod
    def user_update(request):
        # Query user
        result = db.session.execute(db.select(models.User).filter_by(email=request.values.get('user_email'))).all()
        # Assign user
        if len(result) > 0:
            new_found_user = result[0][0]
        else:
            return print('Usuário não encontrado!')
        if not request.form:
            return print('Nenhum parâmetro pra modificar!')
        # Check parameter is in dict
        keys = ['username', 'email', 'password']
        for key in keys:
            if key in request.form.keys():
                if request.form[key] != "":
                        setattr(new_found_user, key, request.form[key])
        # Hash Passwd
        if 'password' in request.form.keys():
            hash, _ = Controller.hash_passwd(request.form['password'])
            new_found_user.password = hash
        else:
            new_found_user.password = ""
        # If changed some parameter, try login to validate
        try:
            db.session.commit()
        except:
            return print('Erro no Commit!')
        # Test users
        return print('Usuário atualizado com sucesso!')


    @staticmethod
    def user_delete(request):
        result = db.session.execute(db.select(models.User).filter_by(email=request.values.get('user_data'))).all()
        if len(result) > 0:
            found_user = result[0][0]
        else:
            return print('Erro! Usuário não encontrado!')
        if found_user.username == "Admin":
            return print('Erro! Admin não pode ser excluído!')
        if found_user.email == session['user_logged']:
            return print('Erro! Impossível realizar auto-exclusão!')
        else:
            found_user.active = 0
            db.session.commit()
            return print(f'Usuário {found_user.username} excluído!')