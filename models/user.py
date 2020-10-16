from models.base_model import BaseModel
from werkzeug.security import generate_password_hash
import peewee as pw


class User(BaseModel):
    username = pw.CharField()
    email = pw.CharField(unique=True)
    password = pw.TextField()

    def validate(self):
        duplicate_emails = User.get_or_none(User.email == self.email)
        if duplicate_emails:
            self.error.append('There is an existing account with this email address')
        else:
            self.password = hashed_password = generate_password_hash(self.password)
