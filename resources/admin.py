from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from db import db
from models import UserModel
from schemas import UserRoleSchema, UserSchema

blp = Blueprint("admin", __name__, description="Administration operations")


@blp.route("/admin/users/<int:user_id>")
class UserRole(MethodView):
    @jwt_required()
    @blp.arguments(UserRoleSchema)
    @blp.response(200, UserSchema)
    def put(self, role_data, user_id):
        user = UserModel.query.get_or_404(user_id)
        user.role = role_data["role"]
        db.session.add(user)
        db.session.commit()
        return user
