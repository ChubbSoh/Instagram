from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from app import app, db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from app.users.models import User
from app.users.forms import RegistrationForm, LoginForm
from flask_login import LoginManager, login_required, login_user, logout_user


sessions_blueprint = Blueprint('sessions', __name__, template_folder='templates')

login_manager.init_app(app)




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@sessions_blueprint.route('/')
# @login_required
def home():
    flash('You have been logged in!')
    return render_template('home.html')

 
@sessions_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data): 
            login_user(user, remember=True)
            return redirect(url_for('sessions.home')) 
        else:
            flash('Login unsucessful. Please check your username or password')
    return render_template('login.html', title='Login', form=form)

@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    flash('You are logged out!')
    return redirect(url_for('sessions.login'))
