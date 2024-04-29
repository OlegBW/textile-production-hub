from db import db
from .shared import TableRepr


class UserModel(db.Model, TableRepr):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    logs = db.relationship(
        "LogModel", back_populates="user", lazy="dynamic", cascade="all, delete"
    )
    reports = db.relationship(
        "ProductionReportModel",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete",
    )
