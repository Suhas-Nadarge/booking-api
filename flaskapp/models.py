from flaskapp import db , login_manager
# This will allow us to use is_authenticated , is_active ,methods for current_user
from flask_login import UserMixin 
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(20),unique=False,nullable=False)
    lastname = db.Column(db.String(20),unique=False,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    isDoctor = db.Column(db.Boolean, default=False, nullable=False)
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"User('{self.firstname},{self.email}')"



class Booking(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    reason = db.Column(db.String(120),nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False,default=datetime.now())
    additional_comments = db.Column(db.Text, nullable=False)
    slot_number = db.Column(db.Integer,nullable=False)
    slot = db.Column(db.String(120),nullable=False)
    patient_id = db.Column(db.Integer,nullable=False)
    doctors_id = db.Column(db.Integer,nullable=False)
    isCancelled = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return str(self.patient_id)

