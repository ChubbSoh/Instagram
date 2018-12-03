from app import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from app.config import Config

class Image(UserMixin, db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_name = db.Column(db.String)
    donation = db.relationship("Donation", backref='image')

    def __init__(self, user_id, image_name):
        self.user_id = user_id
        self.image_name = image_name

    @hybrid_property
    def image_url(self):
        return f"{Config.S3_LOCATION}{self.image_name}"


class Donation(UserMixin, db.Model):

    __tablename__ = 'donation'

    transaction_id = db.Column(db.Integer, primary_key=True )
    amount = db.Column(db.Integer)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))

    def __init__(self, amount, transaction_id):
        self.amount = amount

