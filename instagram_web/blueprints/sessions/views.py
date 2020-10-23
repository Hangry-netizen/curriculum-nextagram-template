import peeweedbevolve
import os
from flask import Blueprint, render_template, url_for, flash, redirect, request
from models.user import *
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user
from instagram_web.util.google_oauth import oauth

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
            flash("Incorrect password")
            return redirect(url_for("sessions.new"))
    else:
        flash("Username not found")
        return redirect(url_for("sessions.new"))

@sessions_blueprint.route('/delete', methods=['POST'])
@login_required
def destroy():
    logout_user()
    return redirect("/")

@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        return redirect(url_for('users.show', username=user.username))
    else:
        flash("Log in failed. Please try again.")
        return redirect(url_for('sessions.new'))
