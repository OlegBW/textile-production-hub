import random
import click

from db import db
from models import ProcessedProductionDataModel


def generate_mock_records():
    data = []

    for i in range(10):
        report = {
            "req_finish_fabrics": round(random.uniform(100, 500), 2),
            "fabric_allowance": round(random.uniform(5, 20), 2),
            "rec_beam_length_yds": round(random.uniform(100, 500), 2),
            "shrink_allow": round(random.uniform(1, 5), 2),
            "req_grey_fabric": round(random.uniform(100, 500), 2),
            "req_beam_length_yds": round(random.uniform(100, 500), 2),
            "total_pdn_yds": round(random.uniform(100, 500), 2),
            "warp_count": random.randint(100, 500),
            "weft_count": random.randint(100, 500),
            "epi": random.randint(10, 30),
            "ppi": random.randint(10, 30),
            "rejection": round(random.uniform(0, 10), 2),
        }

        db_record = ProcessedProductionDataModel(**report)
        data.append(db_record)
        return data


@click.command("seed-db")
def load_fixtures():
    "add fixtures to the database"
    db.create_all()
    records = generate_mock_records()

    db.session.add_all(records)
    db.session.commit()
