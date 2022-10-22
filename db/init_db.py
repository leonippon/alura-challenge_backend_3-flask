from controllers.database_users_cd import Controller as dbUCD
from flask import current_app
import db.models as models


# Startup
db = current_app.extensions['sqlalchemy']


# Check/Create Tables
with current_app.app_context():
    db.create_all()


# Check Admin
admin = models.User(email="admin@email.com.br", username="Admin", password="123999")
result = db.session.execute(db.select(models.User).filter_by(email=admin.email)).all()
if len(result) == 0:
    dbUCD.user_create(admin)


# Create Test Users
if current_app.config['TEST_USERS'] == True:
    # USER 1
    user1 = models.User(email="user1@email.com.br", username="User1")
    result = db.session.execute(db.select(models.User).filter_by(email=user1.email)).all()
    if len(result) == 0:
        dbUCD.user_create(user1)
    # USER 2
    user2 = models.User(email="user2@email.com.br", username="User2")
    result = db.session.execute(db.select(models.User).filter_by(email=user2.email)).all()
    if len(result) == 0:
        dbUCD.user_create(user2)
    # USER 3
    user3 = models.User(email="user3@email.com.br", username="User3")
    result = db.session.execute(db.select(models.User).filter_by(email=user3.email)).all()
    if len(result) == 0:
        dbUCD.user_create(user3)