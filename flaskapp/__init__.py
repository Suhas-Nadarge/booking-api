from flask import Flask , request
from flask_cors import CORS , cross_origin 
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_mail import Mail

app = Flask(__name__)



CORS(app)

app.config['SECRET_KEY'] = '33031f10631062e325547a964ef12b3d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_ID')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'acereddy8053@gmail.com'
mail = Mail(app)

db = SQLAlchemy(app)

#for passswd hashing 
bcrypt = Bcrypt(app)


# to handle user login
login_manager = LoginManager(app)
# to tell where to check login view
login_manager.login_view = 'login'


from flaskapp import routes