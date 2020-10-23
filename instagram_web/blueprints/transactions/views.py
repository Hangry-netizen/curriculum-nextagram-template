from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user
from models.image import Image
from models.user import User
from models.transaction import Transaction
from helpers import get_client_token, create_transaction
from braintree.successful_result import SuccessfulResult


transactions_blueprint = Blueprint('transactions',
                            __name__,
                            template_folder='templates')


@transactions_blueprint.route('/new', methods=['GET'])
def new(image_id):
    return render_template('transactions/new.html', client_token=get_client_token(), image_id=image_id)

@transactions_blueprint.route('/', methods=['POST'])
def create(image_id):
    data = request.form
    image = Image.get_by_id(image_id)
    
    result = create_transaction(data.get("amount"), data.get("payment_method_nonce"))
    if type(result) == SuccessfulResult:
        new_transaction = Transaction(amount=data.get("amount"), image=image, user=current_user.id)
        if new_transaction.save():
            return redirect(url_for('users.show', username=image.user.username))
        else:
            flash("Couldn't save transaction")
            return redirect(url_for("transactions.new", image_id=image_id))
    else:
        flash("Couldn't create braintree transaction")
        return redirect(url_for("transactions.new", image_id=image_id))