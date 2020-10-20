import peeweedbevolve
import os
from flask import Blueprint, render_template, url_for, flash, redirect, request
from models.user import *
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    user = User.get_or_none(User.username == request.form.get('username'))
    if user:
        password_to_check = request.form.get('password')
        hashed_password = user.password_hash
        result = check_password_hash(hashed_password, password_to_check)
        if result:
            login_user(user)
            return redirect("/")
        else:
            return "Incorrect password"
    else:
        return redirect(url_for("sessions.new"))

@sessions_blueprint.route('/delete', methods=['POST'])
@login_required
def destroy():
    logout_user()
    return redirect("/")

@sessions_blueprint.route('/<username>', methods=["GET"])
def show(username):
    return "User's Profile Page"


@sessions_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@sessions_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):

    pass


@sessions_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
