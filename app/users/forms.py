import re
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from sqlalchemy.orm import validates
from app.users.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# from Instagram.helpers import validation_preparation


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class EditUserForms(FlaskForm):

    username = StringField('Username:')
    email = StringField('Email:')
    description = TextAreaField('Description:')
    private = BooleanField('Make Private')
    picture =  FileField('Update Profile Picture', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    submit = SubmitField('Update:')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different email')   



    # @validates('username')
    # @validation_preparation
    # def validate_username(self, key, username):
    #     if not username:
    #         self.validation_errors.append('No username provided')

    #     if (not self.username == username):
    #         if User.query.filter_by(username=username).first():
    #             self.validation_errors.append('Username is already in use')

    #     if len(username) < 5 or len(username) > 20:
    #         self.validation_errors.append(
    #             'Username must be between 5 and 20 characters')

    #     return username

    # @validates('email')
    # @validation_preparation
    # def validate_email(self, key, email):
    #     if not email:
    #         self.validation_errors.append('No email provided')

    #     if not re.match("[^@]+@[^@]+\.[^@]+", email):
    #         self.validation_errors.append(
    #             'Provided email is not an email address')

    #     if (not self.email == email):
    #         if User.query.filter_by(email=email).first():
    #             self.validation_errors.append('Email is already in use')

    #     return email

    # @validation_preparation
    # def set_password(self, password):
    #     if not password:
    #         self.validation_errors.append('Password not provided')

    #     if len(password) < 8 or len(password) > 50:
    #         self.validation_errors.append(
    #             'Password must be between 8 and 50 characters')

    #     self.password_hash = generate_password_hash(password)