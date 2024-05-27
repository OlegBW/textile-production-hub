import joblib
import pandas as pd

model = joblib.load("ml_models/model.pkl")


def predict(data):
    prediction_data = pd.DataFrame.from_records([data])

    result = model.predict(prediction_data)[0]
    return result


def predict_bulk(csv_file):
    prediction_data = pd.read_csv(csv_file)

    predictions = model.predict(prediction_data)

    result_df = pd.DataFrame(predictions, columns=["Prediction"])

    result_data = pd.concat([prediction_data, result_df], axis=1)

    csv_output = result_data.to_csv(index=False)

    return csv_output
