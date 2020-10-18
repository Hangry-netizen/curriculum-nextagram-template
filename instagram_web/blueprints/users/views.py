import peeweedbevolve

from flask import Blueprint, render_template, url_for, flash, redirect, request
from models.user import *


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    new_user = User(
        username=request.form.get('username'),
        email=request.form.get('email'),
        password=request.form.get('password'))
    if new_user.save():
        flash("Signed up successfully!")
        return redirect("/")
    else:
        for error in new_user.errors:
            flash(error)
        return redirect(url_for("users.new"))

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
