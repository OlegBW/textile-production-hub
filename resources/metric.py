from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

blp = Blueprint("metrics", __name__, description="Metrics for data visualization")


@blp.route("/metrics/rejection")
class RejectionMetrics(MethodView):
    @jwt_required()
    def get(self):
        pass
