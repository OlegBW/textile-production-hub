from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from flask import request, send_file
import io

from schemas import PredictionInputSchema, PredictionBulkSchema
from lib.prediction import predict, predict_bulk
from lib.decorators.role_required import role_required
from lib.decorators.limit_content_length import limit_content_length
from lib.logs import log

blp = Blueprint("predictions", __name__, description="Operations on predictions")


@blp.route("/prediction")
class Prediction(MethodView):
    @jwt_required()
    @role_required(["user"])
    @blp.arguments(PredictionInputSchema)
    def post(self, prediction_data):
        jwt_sub = get_jwt_identity()
        user_id = jwt_sub["id"]

        forecast = predict(prediction_data)
        log("Get a prediction", user_id)
        return {"result": forecast}, 200


@blp.route("/prediction/bulk")
class PredictionBulk(MethodView):
    @jwt_required()
    @role_required(["user"])
    @blp.arguments(PredictionBulkSchema, location="files")
    def post(self, prediction_data):
        jwt_sub = get_jwt_identity()
        user_id = jwt_sub["id"]
        forecast_csv = predict_bulk(prediction_data["file"])

        log("Get a bulk prediction", user_id)

        return send_file(
            io.BytesIO(forecast_csv.encode()),
            as_attachment=True,
            download_name="result.csv",
            mimetype="text/csv",
        )
