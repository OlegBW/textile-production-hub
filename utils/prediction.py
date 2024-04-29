import joblib
import pandas as pd

model = joblib.load("ml_models/model.pkl")


def predict(data):
    prediction_data = pd.DataFrame.from_records([data])

    result = model.predict(prediction_data)[0]
    return result


def predict_bulk(csv_file):
    prediction_data = pd.read_csv(csv_file)

    result = list(model.predict(prediction_data))
    return result
