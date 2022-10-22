from flask import current_app
import uuid as uuid_pkg

# Startup
db = current_app.extensions['sqlalchemy']

class Transaction(db.Model):
    __tablename__ = "transactions"
    # FIELDS
    id = db.Column(db.VARCHAR(45), primary_key=True, nullable=False, unique=True, default=uuid_pkg.uuid4())
    origin_bank = db.Column(db.VARCHAR(50), nullable=False)
    origin_agency = db.Column(db.VARCHAR(4), nullable=False)
    origin_account = db.Column(db.VARCHAR(7), nullable=False)
    destination_bank = db.Column(db.VARCHAR(50), nullable=False)
    destination_agency = db.Column(db.VARCHAR(4), nullable=False)
    destination_account = db.Column(db.VARCHAR(7), nullable=False)
    transaction_value = db.Column(db.INTEGER, nullable=False)
    transaction_date = db.Column(db.DATE, nullable=False)
    upload_date = db.Column(db.DATE, nullable=False)
    upload_user_email = db.Column(db.ForeignKey('users.email'), nullable=False)
    # RELATIONSHIP
    upload_user = db.relationship('User', backref='users')
    # METHODS
    def __repr__(self):
        return f"Transaction(id={self.id!r}, value={self.transaction_value!r}, date={self.transaction_date!r}, upload_user={self.upload_user!r})"

class User(db.Model):
    __tablename__ = "users"
    # FIELDS
    email = db.Column(db.VARCHAR(30), nullable=False, primary_key=True, unique=True)
    username = db.Column(db.VARCHAR(15), nullable=False, unique=True)
    password = db.Column(db.VARCHAR(36), nullable=False)
    active = db.Column(db.VARCHAR(1), nullable=False, default=1)
    # METHODS
    def __repr__(self):
        return f"User(username={self.username!r}, email={self.email!r})"