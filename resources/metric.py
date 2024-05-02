from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from db import db
from models import ProcessedProductionDataModel
from schemas import ConstructionSchema

blp = Blueprint("metrics", __name__, description="Metrics for data visualization")

# Прийняти конструкції
# Зробити запит БД на отримання середнього значення відходів
# Повернути отримані з БД метрики

# avg_rejection = db.session.query(
#     db.func.avg(ProcessedProductionDataModel.rejection)
# ).scalar()


@blp.route("/metrics/rejection")
class RejectionMetrics(MethodView):
    @jwt_required()
    @blp.arguments(ConstructionSchema(many=True))
    def post(self, constructions):
        metrics = []

        for construction in constructions:
            metrica = (
                db.session.query(
                    (
                        (
                            db.func.sum(ProcessedProductionDataModel.rejection)
                            / db.func.sum(ProcessedProductionDataModel.total_pdn_yds)
                        )
                        * 100
                    ).label("rejection_percentage")
                )
                .where(
                    ProcessedProductionDataModel.warp_count
                    == construction["warp_count"],
                    ProcessedProductionDataModel.weft_count
                    == construction["weft_count"],
                    ProcessedProductionDataModel.epi == construction["epi"],
                    ProcessedProductionDataModel.ppi == construction["ppi"],
                )
                .scalar()
            )
            metrics.append(metrica)
        return {"result": metrics}
