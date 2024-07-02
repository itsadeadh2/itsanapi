from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required,
    create_refresh_token,
    get_jwt_identity
)

from src.infrastructure.schemas import UserSchema

bp = Blueprint("Users", __name__, description="Operations on users")


@bp.route('/api/login')
class UserLogin(MethodView):
    @bp.arguments(UserSchema)
    def post(self, user_data):
        if user_data['username'] == 'admin':
            access_token = create_access_token(identity='admin')
            return {"access_token": access_token}, 200
        abort(401, message="Invalid credentials.")


@bp.route('/api/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        #jti = get_jwt()["jti"]
        #expired_token = ExpiredTokensModel(jti=jti)
        #db.session.add(expired_token)
        #db.session.commit()
        return {"message": "Successfully logged out"}, 200
