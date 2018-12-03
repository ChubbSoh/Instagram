from app import db, app
from flask_login import UserMixin
from flask import url_for
from sqlalchemy.ext.hybrid import hybrid_property
from app.config import Config



class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.Text())
    description = db.Column(db.Text())
    profile_picture = db.Column(db.String)
    images = db.relationship("Image", backref='user', lazy=True)
    private = db.Column(db.Boolean)

    def __init__(self,username,email, password):
        self.username = username
        self.email = email
        self.password = password
        

    def __repr__(self):
        return '<User %r>' % self.username

    @hybrid_property
    def profile_picture_url(self):
        return f"{Config.S3_LOCATION}{self.profile_picture}"



    


