import peeweedbevolve
from models.image import *
from flask import Blueprint, render_template, url_for, flash, redirect, request
from helpers import upload_file_to_s3
from flask_login import login_required, current_user

images_blueprint = Blueprint('images',
                                __name__,
                                template_folder='templates')


@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('images/new.html')

@images_blueprint.route('/', methods=['POST'])
@login_required
def create():
    file = request.files["user_image"]

    if file.filename == "":
        return flash("Please select a file")
    
    if file:
        file_path = upload_file_to_s3(file=file, folder_name="user-img")

        new_image = Image(user=current_user.id, image_url=file_path)

        if new_image.save():
            return redirect(url_for('users.show', username=current_user.username))
        else:
            flash("Image upload failed. Please try again")
            return redirect(url_for('images.new'))

    else:
        return redirect(url_for("images.new"))
        