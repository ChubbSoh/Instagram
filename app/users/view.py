from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from app.users.models import User
from app.users.forms import RegistrationForm, LoginForm, EditUserForms
from app.helpers import upload_file_to_s3, generate_client_token, find_transaction, transact
from werkzeug.utils import secure_filename
from app.images.form import UserImageForm
from app.config import Config
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from app.config import gateway
import braintree
from app.images.model import Donation


users_blueprint = Blueprint('users', __name__, template_folder="templates")

@users_blueprint.route("/sign_up", methods=["POST", "GET"])
def create():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        form = RegistrationForm()
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
    
        flash(f'Account created for {form.email.data}!', 'sucess')
        return redirect(url_for('sessions.home'))
    return render_template('users/register.html', title='Register', form=form )

@users_blueprint.route('/account', methods=["GET","POST"])
@login_required
def account():     
    form = UserImageForm()
    return render_template("users/account.html", form=form)

@users_blueprint.route('/edit/<id>', methods=["GET","POST"])
@login_required
def edit(id):
    form = EditUserForms(request.form)
    user = User.query.get(id)

    if user.id == current_user.id and form.validate_on_submit():
        user = User.query.get(id)
        user.username = form.username.data
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash ('Your details have been updated!')
        return render_template('users/show.html', form=form, id = current_user.id)
    else:
        
        return render_template('users/edit.html', form=form, user=user)
 

@users_blueprint.route("/<id>/profile/images", methods=["POST"])
@login_required
def upload_profile_picture(id):
    form = EditUserForms()
    user =User.query.get(id)
    file = form.picture.data

    if not user.id == current_user.id:
        return render_template('users/edit.html', validation_error=['Unauthorized!'], form=form, user=user)

    if file.filename =="":
        flash("Please select a file")
        return render_template('users/edit.html', form=form)

    if file:
        file.filename = secure_filename(user.username + "-" + file.filename)
        output = upload_file_to_s3(file, Config.S3_BUCKET)
        user.profile_picture = file.filename
        profile_picture = ("https://s3.amazonaws.com/chubb-clone-instagram/" + user.profile_picture)

        db.session.add(user)
        db.session.commit()

        flash("Profile Updated")

        return redirect(url_for('users.edit', id = current_user.id, username=user.username, profile_picture = profile_picture, form=form))



@users_blueprint.route("/client_token", methods=["GET"])
def client_token():
  return gateway.client_token.generate()

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

@users_blueprint.route('/checkout', methods=['GET'])
def index():
    return redirect(url_for('users.new_checkout'))

@users_blueprint.route('/<id>', methods=['GET'])
def show(id):
    return redirect(url_for('users.new_checkout', image_id=id))

@users_blueprint.route('/checkouts/new', methods=['GET'])
def new_checkout():
    client_token = generate_client_token()
    return render_template('users/new.html', client_token=client_token)

@users_blueprint.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('users/show.html', transaction=transaction, result=result)

@users_blueprint.route('/checkouts', methods=['POST'])
def create_checkout():
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        return redirect(url_for('users.show_checkout',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('users.new_checkout'))
