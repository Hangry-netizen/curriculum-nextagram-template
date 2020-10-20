from models.base_model import BaseModel
from werkzeug.security import generate_password_hash
import peewee as pw
import re
from flask_login import UserMixin

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password_hash = pw.CharField(unique=False)
    password = None

    def validate(self):
        duplicate_email = User.get_or_none(User.email == self.email)
        duplicate_username = User.get_or_none(User.username == self.username)
        print("User validation in process")
        if duplicate_email:
            self.errors.append("There is an existing account with this email address")

        if duplicate_email:
            self.errors.append("Username taken!")

        if self.password:
            if len(self.password) < 6:
                self.errors.append("Password has to be at least 6 characters")
            if not re.search("[a-z]", self.password):
                self.errors.append("Password must contain at least one lowercase letter")
            if not re.search("[A-Z]", self.password):
                self.errors.append("Password must contain at least one uppercase letter")
            if not re.search("[\!\@\#\$\%\^\&\*\(\)\[\]\{\}\;\:\<\>\?\/]", self.password):
                self.errors.append("Password must contain at least one special character")
            if len(self.errors) == 0:
                print("No erros detected")
                self.password_hash= generate_password_hash(self.password)
        elif not self.password_hash:
            self.errors.append('Password is required')