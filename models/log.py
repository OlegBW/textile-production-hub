from db import db
from .shared import TableRepr


class LogModel(db.Model, TableRepr):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("UserModel", back_populates="logs")
