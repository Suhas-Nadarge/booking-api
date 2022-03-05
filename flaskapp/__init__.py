from flask import Flask , request
from flask_cors import CORS , cross_origin 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


app = Flask(__name__)



CORS(app)

app.config['SECRET_KEY'] = '33031f10631062e325547a964ef12b3d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)



# to handle user login
login_manager = LoginManager(app)
# to tell where to check login view
login_manager.login_view = 'login'


from flaskapp import routes