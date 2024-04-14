import os
from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from db import db
from resources.user import blp as UserBlueprint
from resources.prediction import blp as PredictionBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Forecast REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    api = Api(app)  # noqa: F841
    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)  # noqa: F841

    app.config["JWT_SECRET_KEY"] = "5446649551128884611"
    jwt = JWTManager(app)  # noqa: F841

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(PredictionBlueprint)
    return app
