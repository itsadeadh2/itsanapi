from src.database.models import UserModel
from flask_sqlalchemy import SQLAlchemy
from src.infrastructure.schemas import UserSchema
from marshmallow import ValidationError
from logging import Logger
from injector import inject


class UserService:

    @inject
    def __init__(self, db: SQLAlchemy, logger: Logger, user_schema: UserSchema):
        self.__db = db
        self.__user_schema = user_schema
        self.__logger = logger

    def get_user_by_email(self, email: str) -> bool | dict:
        self.__logger.debug(f"Fetching user with email: {email}")
        user = UserModel.query.filter(UserModel.email == email).first()
        if user:
            self.__logger.info(f"User found with email: {email}")
            return self.__user_schema.dump(user)
        self.__logger.info(f"No user found with email: {email}")
        return False

    def get_validated_data(self, user_data):
        try:
            validated_data = self.__user_schema.load(user_data)
            self.__logger.debug(f"User data validated: {validated_data}")
            return validated_data
        except ValidationError as err:
            self.__logger.error(f"Validation error: {err.messages}")
            raise err

    def add_user_to_db(self, user_data):
        # If validation is successful, create the user
        new_user = UserModel(**user_data)
        self.__logger.debug(f"New user model created: {new_user}")

        try:
            self.__db.session.add(new_user)
            self.__db.session.commit()
            self.__logger.info(f"New user created with ID: {new_user.id}")
            return new_user
        except Exception as e:
            self.__logger.error(f"Error committing new user to the database: {str(e)}")
            self.__db.session.rollback()
            raise e

    def create_user(self, user_data) -> dict:
        self.__logger.debug("Starting user creation process.")
        validated_data = self.get_validated_data(user_data)
        # If the user already exists, just return him
        existing_user = self.get_user_by_email(email=validated_data['email'])
        if existing_user:
            self.__logger.warning(f"User already exists with email: {validated_data['email']}")
            return existing_user
        new_user = self.add_user_to_db(validated_data)
        return self.__user_schema.dump(new_user)
