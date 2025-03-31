from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, password, name="", last_name="", phone="", address="") -> None:
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.last_name = last_name
        self.phone = phone
        self.address = address

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)

    @classmethod
    def hash_password(cls, password):
        return generate_password_hash(password)
