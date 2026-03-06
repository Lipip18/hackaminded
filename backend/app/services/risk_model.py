import joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest

MODEL_PATH = Path("app/models/risk_model.pkl")

FEATURE_COLUMNS = [
    "Declared_Value",
    "Declared_Weight",
    "Measured_Weight",
    "Dwell_Time_Hours",
    "Weight_Diff",
    "Weight_Diff_Pct",
    "Value_Per_Weight",
    "Importer_Frequency",
    "Exporter_Frequency",
    "Shipping_Line_Frequency",
    "Route_Frequency",
    "HS_Code_Frequency",
    "Off_Hours_Declaration",
    "Weekend_Declaration",
]


def train_model(features: pd.DataFrame):

    X = features[FEATURE_COLUMNS]

    model = IsolationForest(
        n_estimators=150,
        contamination=0.1,
        random_state=42
    )

    model.fit(X)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    return model


def load_model():

    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)

    raise FileNotFoundError("Model not trained yet.")


def predict_risk(features: pd.DataFrame):

    model = load_model()

    X = features[FEATURE_COLUMNS]

    anomaly_prediction = model.predict(X)
    anomaly_score = model.decision_function(X)

    risk_score = (1 - anomaly_score) * 100

    risk_level = []

    for score in risk_score:

        if score > 70:
            risk_level.append("Critical")

        elif score > 40:
            risk_level.append("Medium")

        else:
            risk_level.append("Low Risk")

    score_components = {
        "model_score": risk_score
    }

    return risk_score, risk_level, score_components