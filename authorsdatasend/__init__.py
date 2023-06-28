from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
app = Flask(__name__, template_folder='templates')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

mail = Mail(app)

migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = u'Пожалуйста, войдите, чтобы получить доступ к этой странице.'

import authorsdatasend.views
import authorsdatasend.admin_views