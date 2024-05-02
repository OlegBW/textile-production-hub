from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from db import db
from models import (
    UserModel,
    LogModel,
    ProductionReportModel,
    ProcessedProductionDataModel,
)
from schemas import UserRoleSchema, UserSchema, LogSchema

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


@blp.route("/admin/logs")
class LogList(MethodView):
    @jwt_required()
    @blp.paginate()
    @blp.response(200, LogSchema(many=True))
    def get(self, pagination_parameters):
        total_items = LogModel.query.count()
        pagination_parameters.item_count = total_items

        page_size = pagination_parameters.page_size
        page = pagination_parameters.page

        log_page = LogModel.query.limit(page_size).offset((page - 1) * page_size).all()
        return log_page


@blp.route("/admin/reports/<int:report_id>/submit")
class Report(MethodView):
    @jwt_required()
    def post(self, report_id):
        report = ProductionReportModel.query.get_or_404(report_id)

        processed_data = ProcessedProductionDataModel(
            **{
                "req_finish_fabrics": report.req_finish_fabrics,
                "fabric_allowance": report.fabric_allowance,
                "rec_beam_length_yds": report.rec_beam_length_yds,
                "shrink_allow": report.shrink_allow,
                "req_grey_fabric": report.req_grey_fabric,
                "req_beam_length_yds": report.req_beam_length_yds,
                "total_pdn_yds": report.total_pdn_yds,
                "warp_count": report.warp_count,
                "weft_count": report.weft_count,
                "epi": report.epi,
                "ppi": report.ppi,
                "rejection": report.rejection,
            }
        )

        db.session.delete(report)
        db.session.add(processed_data)
        db.session.commit()

        return {"msg": "Report approved"}
