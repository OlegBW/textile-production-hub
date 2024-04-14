from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from schemas import PredictionInputSchema, PredictionBulkSchema
from utils.forecast import predict, predict_bulk

blp = Blueprint("predictions", __name__, description="Operations on predictions")


@blp.route("/prediction")
class Prediction(MethodView):
    # jwt.required()
    @blp.arguments(PredictionInputSchema)
    def post(self, prediction_data):
        forecast = predict(prediction_data)
        return {"forecast": forecast}, 200


@blp.route("/prediction/bulk")
class PredictionBulk(MethodView):
    # jwt.required()
    @blp.arguments(PredictionBulkSchema, location="files")
    def post(self, prediction_data):
        forecast = predict_bulk(prediction_data["file"])
        return {"forecast": forecast}, 200
