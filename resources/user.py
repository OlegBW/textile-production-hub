from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

from schemas import UserRegisterSchema, UserLoginSchema, UserSchema
from db import db
from lib.password import get_password_hash, verify_password
from models import UserModel

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        user_data["password"] = get_password_hash(user_data["password"])

        try:
            new_user = UserModel(**user_data, role="user")
            db.session.add(new_user)
            db.session.commit()
            return {"msg": "User created"}, 201
        except IntegrityError:
            return {"msg": "User already exists"}, 400


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_credentials):
        user = UserModel.query.filter(
            UserModel.email == user_credentials["email"]
        ).first()

        if user and verify_password(user.password, user_credentials["password"]):
            access_token = create_access_token(
                identity={"id": user.id, "role": user.role}
            )
            return {"access_token": access_token}

        abort(401)


@blp.route("/users/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
