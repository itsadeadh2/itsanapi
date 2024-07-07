from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256

from src.database.models import UserModel, ExpiredTokensModel
from src.infrastructure.exc import UserAlreadyExists, InvalidCredentials
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity
)


class UserService:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create_user(self, user_data):
        if UserModel.query.filter(UserModel.email == user_data['email']).first():
            raise UserAlreadyExists("User already exists")
        user = UserModel(
            name=user_data["name"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def log_in_user(self, user_data):
        try:
            user = self.get_user_by_email(user_data.get('email'))
            password_match = self.check_user_password(
                given_password=user_data.get('password'),
                encrypted_password=user.password
            )
            if user and password_match:
                return self.create_token(user_id=user.id)
            else:
                raise InvalidCredentials("Invalid credentials")
        except Exception:
            raise InvalidCredentials("Invalid credentials")

    def log_out_user(self):
        jti = get_jwt()["jti"]
        expired_token = ExpiredTokensModel(jti=jti)
        self.db.session.add(expired_token)
        self.db.session.commit()

    def get_user_by_email(self, email):
        user = UserModel.query.filter(
            UserModel.email == email
        ).first()
        return user

    def get_user_from_token(self):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        return user

    def check_user_password(self, given_password, encrypted_password):
        return pbkdf2_sha256.verify(given_password, encrypted_password)

    def create_token(self, user_id):
        return create_access_token(identity=user_id)
