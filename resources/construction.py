from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from db import db
from models import ProcessedProductionDataModel
from schemas import ConstructionSchema

blp = Blueprint("construction", __name__, description="Available textile constructions")


@blp.route("/constructions")
class AvailableConstructions(MethodView):
    @jwt_required()
    @blp.paginate()
    @blp.response(200, ConstructionSchema(many=True))
    def get(self, pagination_parameters):
        total_items = (
            db.session.query(
                ProcessedProductionDataModel.warp_count,
                ProcessedProductionDataModel.weft_count,
                ProcessedProductionDataModel.epi,
                ProcessedProductionDataModel.ppi,
            )
            .distinct(
                ProcessedProductionDataModel.warp_count,
                ProcessedProductionDataModel.weft_count,
                ProcessedProductionDataModel.epi,
                ProcessedProductionDataModel.ppi,
            )
            .count()
        )

        pagination_parameters.item_count = total_items

        page_size = pagination_parameters.page_size
        page = pagination_parameters.page

        constructions = (
            db.session.query(
                ProcessedProductionDataModel.warp_count,
                ProcessedProductionDataModel.weft_count,
                ProcessedProductionDataModel.epi,
                ProcessedProductionDataModel.ppi,
            )
            .distinct(
                ProcessedProductionDataModel.warp_count,
                ProcessedProductionDataModel.weft_count,
                ProcessedProductionDataModel.epi,
                ProcessedProductionDataModel.ppi,
            )
            .limit(page_size)
            .offset((page - 1) * page_size)
            .all()
        )

        return constructions
