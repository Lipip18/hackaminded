import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from app.config import settings


def _mad_score(series: pd.Series) -> pd.Series:
    """
    Compute Median Absolute Deviation score for anomaly detection
    """
    median = series.median()
    mad = (series - median).abs().median()

    if mad == 0:
        return pd.Series(np.zeros(len(series)), index=series.index)

    return ((series - median).abs() / (1.4826 * mad)).clip(0, 8)


def detect_anomalies(features: pd.DataFrame) -> tuple[pd.Series, pd.DataFrame]:
    """
    Detect anomalies using rule-based flags + Isolation Forest model
    """

    # -------- Rule Based Flags --------

    weight_flag = features["Weight_Diff_Pct"] > settings.weight_diff_pct_threshold

    dwell_flag = (
        features["Dwell_Time_Hours"] > settings.dwell_time_threshold_hours
    )

    value_weight_mad = _mad_score(features["Value_Per_Weight"])
    value_flag = value_weight_mad > 3.5

    behavior_flag = (
        (features["Importer_Frequency"] < 0.02)
        & (features["Exporter_Frequency"] < 0.02)
    ) | (features["Route_Frequency"] < 0.01)

    # -------- Model Features --------

    model_features = features[
        [
            "Declared_Value",
            "Declared_Weight",
            "Measured_Weight",
            "Weight_Diff_Pct",
            "Value_Per_Weight",
            "Dwell_Time_Hours",
            "Importer_Frequency",
            "Exporter_Frequency",
            "Route_Frequency",
            "HS_Code_Frequency",
        ]
    ].fillna(0.0)

    # -------- Isolation Forest Model --------

    if len(features) >= 15:

        detector = IsolationForest(
            n_estimators=200,
            contamination=0.12,
            random_state=42,
        )

        detector.fit(model_features)

        decision = detector.decision_function(model_features)

        model_score = 1 - (
            (decision - decision.min())
            / (decision.max() - decision.min() + 1e-9)
        )

        model_score = pd.Series(model_score, index=features.index)

    else:
        model_score = pd.Series(
            np.zeros(len(features)),
            index=features.index
        )

    # -------- Final Anomaly Score --------

    anomaly_score = (
        0.28 * weight_flag.astype(float)
        + 0.18 * dwell_flag.astype(float)
        + 0.22 * value_flag.astype(float)
        + 0.14 * behavior_flag.astype(float)
        + 0.18 * model_score
    ).clip(0, 1)

    # -------- Flags --------

    flags = pd.DataFrame(
        {
            "weight_flag": weight_flag,
            "dwell_flag": dwell_flag,
            "value_flag": value_flag,
            "behavior_flag": behavior_flag,
            "model_flag": model_score > 0.7,
        },
        index=features.index,
    )

    return anomaly_score, flags