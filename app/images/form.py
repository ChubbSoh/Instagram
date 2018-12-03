import re
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from sqlalchemy.orm import validates
from app.users.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class UserImageForm(FlaskForm):
    accountimages =  FileField('Add Pictures', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    submit = SubmitField('Post Image')