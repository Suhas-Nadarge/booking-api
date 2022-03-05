from flaskapp import db , login_manager
# This will allow us to use is_authenticated , is_active ,methods for current_user
from flask_login import UserMixin 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(20),unique=True,nullable=False)
    lastname = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    isDoctor = db.Column(db.Boolean, default=False, nullable=False)
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"User('{self.firstname},{self.email}')"



class 

