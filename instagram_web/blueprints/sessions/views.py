import peeweedbevolve

from flask import Blueprint, render_template, url_for, flash, redirect, request
from models.user import *
from werkzeug.security import check_password_hash

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    current_user = User.get_or_none(User.username == request.form.get('username'))
    if current_user:
        password_to_check = request.form.get('password')
        hashed_password = current_user.password_hash
        result = check_password_hash(hashed_password, password_to_check)
        if result:
            flash('Signed in!')
            return redirect(url_for("sessions.show", username = current_user.username))
    if current_user == None or result == None:
        flash('Incorrect username or password')
        return redirect(url_for("sessions.new"))

@sessions_blueprint.route('/<username>', methods=["GET"])
def show(username):
    return "User's Profile Page"


@sessions_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@sessions_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@sessions_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
