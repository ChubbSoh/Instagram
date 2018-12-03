import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import Config
import braintree
from flask_assets import Bundle, Environment
# from authlib.flask.client import OAuth
# use loginpass to make OAuth connection simpler
#from loginpass import create_flask_blueprint, GitHub
# from app.helpers import oauth
# import config



# This grabs our directory
basedir = os.path.abspath(os.path.dirname(__file__))



app = Flask(__name__, template_folder="static")
# app.config.from_object(os.environ['APP_SETTINGS'])
# oauth.init_app(app)

js = Bundle('js/bootstrap.bundle.min.js', 'js/bootstrap.min.js', 'js/jquery.min.js', 'js/popper.js', output='gen/main.js')


assets = Environment(app)

assets.register('main_js', js)

# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Chubb:@localhost/instagram'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'cc883108399d3ddb3186679bbd56c136'
db = SQLAlchemy(app)

from app.users.models import User

login_manager = LoginManager()
login_manager.login_view = 'sessions.login'

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



from app.users.view import users_blueprint
from app.sessions.view import sessions_blueprint
from app.images.view import image_blueprint




app.register_blueprint(users_blueprint)
app.register_blueprint(sessions_blueprint)
app.register_blueprint(image_blueprint)


# Add on migration capabilities in order to run terminal commands
Migrate(app,db)