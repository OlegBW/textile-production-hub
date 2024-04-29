from db import db
from models import LogModel
from datetime import datetime


def log(message, user_id):
    new_log = LogModel(message=message, user_id=user_id, timestamp=datetime.now())
    db.session.add(new_log)
    db.session.commit()
