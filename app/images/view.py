from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from app.users.models import User
from app.users.forms import RegistrationForm, LoginForm, EditUserForms
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from app.helpers import upload_file_to_s3
from werkzeug.utils import secure_filename
from app.images.model import Image
from app.images.form import UserImageForm
from app.config import Config


image_blueprint = Blueprint('image', __name__)


@image_blueprint.route("/account/create/<id>", methods=["POST","GET"] )
@login_required
def image_create(id):
    form = UserImageForm()
    user = User.query.get(id)
    image = user.images
    file = form.accountimages.data
    
    
    if file:
        file.filename = secure_filename(user.username + "-" + file.filename)
        output = upload_file_to_s3(file, Config.S3_BUCKET)
        user.image_name = file.filename
        image_name = file.filename

        image = Image(user_id=current_user.id, image_name= file.filename)
        
        db.session.add(image)
        db.session.commit()
        flash("Image Posted!")

        return redirect(url_for('users.account', form=form))

    else:
        flash('failed to upload image')
        return redirect("/")
