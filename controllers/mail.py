from flask import current_app
from flask_mail import Message
import os


# Catch Mail
mail = current_app.extensions['mail']


class Controller:
    @staticmethod
    def send_pwd(new_user, passwd):
        # Create Message
        msg = Message(subject='Senha do Sistema',
                        body=f'Seu login é {new_user.username}, e sua senha é {passwd}',
                        recipients=[f'{new_user.email}'],
                        sender='admin@email.com.br'
                        )
        # Send Message
        mail.send(msg)
        # Send Test
        if os.environ.get('FLASK_ENV') != 'production':
            test = Controller.send_testing(msg)
        else:
            test = ""
        # Return
        return test


    @staticmethod
    def send_testing(msg):
        with mail.record_messages() as outbox:
            mail.send(msg)
            print('Mail test message working.')
        return outbox[0].body