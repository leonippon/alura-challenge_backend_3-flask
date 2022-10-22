from flask import current_app, session, flash
import db.models as models
import bcrypt


# Catch DB
db = current_app.extensions['sqlalchemy']


class Controller:
    @staticmethod
    def hash_passwd(passwd):
        bytestream = passwd.encode('utf-8')
        salt_rounds = current_app.config['HASH_SALT_ROUNDS']
        salt = bcrypt.gensalt(salt_rounds)
        hash = bcrypt.hashpw(bytestream, salt)
        return hash, bytestream


    @staticmethod
    def user_auth(req_user, do_session):
        # Check key to find user
        if 'username' in req_user.form.keys():
            key = 'username'
        elif 'email' in req_user.form.keys():
            key = 'email'
        else:
            return print('Usuário não encontrado!')
        # Find user
        result = db.session.execute(db.select(models.User).filter_by(username=req_user.form[key])).all()
        # Auth user
        if len(result) > 0:
            user = result[0][0]
            if user.active == "1":
                _, passwd_bytes = Controller.hash_passwd(req_user.form['password'])
                if bcrypt.checkpw(passwd_bytes, user.password):
                    if do_session:
                        session['user_logged'] = user.email
                    flash(f'Usuário logado com sucesso!')
                    return True
            else:
                print('Erro, usuário excluído!')
                return False
        else:
            print(f'Usuário ou senha inválidos!')
            return False


    @staticmethod
    def user_auth_check():
        if 'user_logged' not in session or session['user_logged'] == None:
            print('NOT LOGGED')
            return False
        else:
            print('IS LOGGED')
            return True


    @staticmethod
    def user_auth_logoff():
        session['user_logged'] = None
        flash(f'Usuário deslogado com sucesso!')