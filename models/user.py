from ..db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80), nullable=False)
    email=db.Column(db.String(80), nullable=False)
    password=db.Column(db.String(256), nullable=False)