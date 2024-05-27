from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from lib.decorators.role_required import role_required
from lib.logs import log

from db import db
from schemas import ProductionDataSchema, ProductionReportSchema
from models import ProductionReportModel

blp = Blueprint(
    "report", __name__, description="Functionality for processing production reports"
)


@blp.route("/reports")
class ProductionReports(MethodView):
    @jwt_required()
    @blp.arguments(ProductionDataSchema)
    def post(self, production_data):
        jwt_sub = get_jwt_identity()
        user_id = jwt_sub["id"]

        new_report = ProductionReportModel(**production_data, user_id=user_id)
        db.session.add(new_report)
        db.session.commit()
        log("Report created", user_id)

        return {"msg": "Report created"}, 201

    @blp.paginate()
    @blp.response(200, ProductionReportSchema(many=True))
    def get(self, pagination_parameters):
        total_items = ProductionReportModel.query.count()
        pagination_parameters.item_count = total_items

        page_size = pagination_parameters.page_size
        page = pagination_parameters.page
        report_page = (
            ProductionReportModel.query.limit(page_size)
            .offset((page - 1) * page_size)
            .all()
        )
        return report_page


@blp.route("/reports/<int:report_id>")
class ProductionReport(MethodView):
    @jwt_required()
    def delete(self, report_id):
        jwt_sub = get_jwt_identity()
        user_id = jwt_sub["id"]

        report = ProductionReportModel.query.get_or_404(report_id)
        db.session.delete(report)
        db.session.commit()
        log(f"Deleted report with ID:{report_id}", user_id)
        return {"msg": "Report deleted"}

    @jwt_required()
    @blp.arguments(ProductionDataSchema)
    def put(self, production_data, report_id):
        jwt_sub = get_jwt_identity()
        user_id = jwt_sub["id"]

        report = ProductionReportModel.query.get(report_id)

        if report:
            report.req_finish_fabrics = production_data["req_finish_fabrics"]
            report.fabric_allowance = production_data["fabric_allowance"]
            report.rec_beam_length_yds = production_data["rec_beam_length_yds"]
            report.shrink_allow = production_data["shrink_allow"]
            report.req_grey_fabric = production_data["req_grey_fabric"]
            report.req_beam_length_yds = production_data["req_beam_length_yds"]
            report.total_pdn_yds = production_data["total_pdn_yds"]
            report.rejection = production_data["rejection"]
            report.warp_count = production_data["warp_count"]
            report.weft_count = production_data["weft_count"]
            report.epi = production_data["epi"]
            report.ppi = production_data["ppi"]

        else:
            report = ProductionReportModel(**production_data, id=report_id)

        db.session.add(report)
        db.session.commit()
        log(f"Updated report with ID:{report_id}", user_id)
        return {"msg": "Report updated"}

    @blp.response(200, ProductionReportSchema)
    def get(self, report_id):
        report = ProductionReportModel.query.get_or_404(report_id)
        return report
