from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from db import db
from models import UserModel
from schemas import UserRoleSchema, UserSchema

from lib.password import get_password_hash

blp = Blueprint("admin", __name__, description="Administration operations")


@blp.route("/admin/users/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get_or_404(user_id)
        user.role = user_data["role"]
        user.username = user_data["username"]
        user.email = user_data["email"]
        user.password = get_password_hash(user_data["password"])
        db.session.add(user)
        db.session.commit()
        return user

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        db.session.delete(user)
        return {"msg": "User deleted"}


@blp.route("/admin/users/<int:user_id>/role")
class UserRole(MethodView):
    @jwt_required()
    @blp.arguments(UserRoleSchema)
    @blp.response(200, UserSchema)
    def patch(self, role_data, user_id):
        user = UserModel.query.get_or_404(user_id)
        user.role = role_data["role"]
        db.session.add(user)
        db.session.commit()
        return user
