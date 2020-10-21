import peeweedbevolve

from flask import Blueprint, render_template, url_for, flash, redirect, request
from models.user import *

from flask_login import login_required, current_user


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
    user = User.get_or_none(User.username == username)
    print(user.username)
    return render_template('users/show.html', user=user)


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_by_id(id)
    # the user we are modifying, based on id from form action
    
    if current_user == user:
        return render_template('users/edit.html')


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    update_user = User.get_by_id(id)
    name = request.form.get('update_username')
    email = request.form.get('update_email')
    password = request.form.get('update_password')
    
    if name != "" or email != "" or password != "":
        update_user.username = name
        update_user.email = email
        update_user.password = password
        if update_user.save():
            flash("Successfully updated your info!")
            return redirect(url_for('users.show', username=User.username))
        else:
            flash("Update was unsuccessful")
            print(update_user.errors)
            return redirect(url_for('users.edit', id=current_user.id))
    else:
        flash("At least one of the fields must be filled")
        return redirect(url_for ('users.edit', id=current-user.id))
