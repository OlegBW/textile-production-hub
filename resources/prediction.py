from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from flask import request

from schemas import PredictionInputSchema, PredictionBulkSchema
from utils.prediction import predict, predict_bulk
from utils.decorators.role_required import role_required
from utils.decorators.limit_content_length import limit_content_length
from utils.logs import log

blp = Blueprint("predictions", __name__, description="Operations on predictions")


@blp.route("/prediction")
class Prediction(MethodView):
    @jwt_required()
    @role_required(["user"])
    @blp.arguments(PredictionInputSchema)
    def post(self, prediction_data):
        forecast = predict(prediction_data)
        return {"result": forecast}, 200


@blp.route("/prediction/bulk")
class PredictionBulk(MethodView):
    @jwt_required()
    @role_required(["user"])
    @blp.arguments(PredictionBulkSchema, location="files")
    def post(self, prediction_data):
        forecast = predict_bulk(prediction_data["file"])
        return {"result": forecast}, 200
