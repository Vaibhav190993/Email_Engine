from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)
app.config.from_object('config.Config')
app.app_context().push()
bcrypt = Bcrypt(app)
mail_app = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
LoginManager.login_view = 'login'
LoginManager.login_message_category = 'info'
from app import views