import joblib
import pandas as pd

model = joblib.load("forecast-model/model.pkl")
print(model.feature_names_in_)

# list_format = [
#     "Req_Finish_Fabrics",
#     "Fabric_Allowance",
#     "Rec_Beam_length(yds)",
#     "Shrink_allow",
#     "Req_grey_fabric",
#     "Req_beam_length(yds)",
#     "Total_Pdn(yds)",
#     "warp_count",
#     "weft_count",
#     "epi",
#     "ppi",
# ]


def predict(data):
    prediction_data = pd.DataFrame.from_records([data])

    result = model.predict(prediction_data)[0]
    return result


def predict_bulk(csv_file):
    prediction_data = pd.read_csv(csv_file)

    result = list(model.predict(prediction_data))
    return result
