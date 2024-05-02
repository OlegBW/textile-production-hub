from db import db
from .shared import TableRepr


class ProductionData(db.Model, TableRepr):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    req_finish_fabrics = db.Column(db.Float, nullable=False)
    fabric_allowance = db.Column(db.Float, nullable=False)
    rec_beam_length_yds = db.Column(db.Float, nullable=False)
    shrink_allow = db.Column(db.Float, nullable=False)
    req_grey_fabric = db.Column(db.Float, nullable=False)
    req_beam_length_yds = db.Column(db.Float, nullable=False)
    total_pdn_yds = db.Column(db.Float, nullable=False)
    warp_count = db.Column(db.Float, nullable=False)
    weft_count = db.Column(db.Float, nullable=False)
    epi = db.Column(db.Integer, nullable=False)
    ppi = db.Column(db.Integer, nullable=False)
    rejection = db.Column(db.Float, nullable=False)


class ProductionReportModel(ProductionData, TableRepr):
    __tablename__ = "production_report"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel", back_populates="reports")


class ProcessedProductionDataModel(ProductionData):
    __tablename__ = "processed_production_data"
