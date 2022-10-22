from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask import Flask
import dotenv
import os


def create_app(config=None):
    # LOAD .env
    dotenv.load_dotenv()


    # Startup APP
    app = Flask(__name__)
    if config is not None:
        app.config.from_object(f'config.{config.get("ENV_CONF")}')
    else:
        app.config.from_object(f'config.{os.environ.get("ENV_CONF")}')


    # Startup DB
    db = SQLAlchemy()
    db.init_app(app)
    # Startup Mail Server
    mail = Mail(app)
    

    # APP Context
    with app.app_context():
        # Import DB stuff
        import db.init_db
        import db.models as models
        # Routes
        from views.views import views
        from views.bp_users import bp_users
        from views.bp_transactions import bp_transactions
        app.register_blueprint(views)
        app.register_blueprint(bp_users)
        app.register_blueprint(bp_transactions)


    return app


# RUN
if __name__ == '__main__':
    create_app()