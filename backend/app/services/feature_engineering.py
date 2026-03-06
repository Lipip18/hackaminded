import numpy as np
import pandas as pd


def _to_numeric(series: pd.Series, default: float = 0.0) -> pd.Series:
    """
    Convert column to numeric safely.
    """
    return pd.to_numeric(series, errors="coerce").fillna(default)


def build_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Build engineered features required for anomaly detection and risk scoring.
    Works for both Historical Data.csv (training) and Real-Time Data.csv (testing).
    """

    features = dataframe.copy()

    # ---------- Date & Time ----------

    if "Declaration_Date" in features.columns:
        features["Declaration_Date"] = pd.to_datetime(
            features["Declaration_Date"], errors="coerce"
        )

    if "Declaration_Time" in features.columns:
        features["Declaration_Time"] = pd.to_datetime(
            features["Declaration_Time"], format="%H:%M:%S", errors="coerce"
        )

    # ---------- Numeric Columns ----------

    numeric_columns = [
        "Declared_Value",
        "Declared_Weight",
        "Measured_Weight",
        "Dwell_Time_Hours",
    ]

    for col in numeric_columns:
        if col in features.columns:
            features[col] = _to_numeric(features[col])
        else:
            features[col] = 0.0

    # ---------- Weight Features ----------

    safe_declared_weight = features["Declared_Weight"].replace(0, np.nan)

    features["Weight_Diff"] = (
        features["Measured_Weight"] - features["Declared_Weight"]
    ).abs()

    features["Weight_Diff_Pct"] = (
        features["Weight_Diff"] / safe_declared_weight
    ).fillna(0.0) * 100

    # ---------- Value Density ----------

    features["Value_Per_Weight"] = (
        features["Declared_Value"] / safe_declared_weight
    ).fillna(0.0)

    # ---------- Trade Regime ----------

    if "Trade_Regime" in features.columns:
        features["Trade_Regime_Import"] = (
            features["Trade_Regime"].astype(str).str.lower() == "import"
        ).astype(int)
    else:
        features["Trade_Regime_Import"] = 0

    # ---------- Route Feature ----------

    if "Origin_Country" in features.columns and "Destination_Country" in features.columns:
        route_series = (
            features["Origin_Country"].astype(str)
            + "->"
            + features["Destination_Country"].astype(str)
        )
    else:
        route_series = "Unknown"

    features["Route"] = route_series

    # ---------- Frequency Encoding ----------

    frequency_columns = [
        ("Importer_ID", "Importer_Frequency"),
        ("Exporter_ID", "Exporter_Frequency"),
        ("Shipping_Line", "Shipping_Line_Frequency"),
        ("Route", "Route_Frequency"),
        ("HS_Code", "HS_Code_Frequency"),
    ]

    for column_name, feature_name in frequency_columns:

        if column_name in features.columns:

            normalized_frequency = (
                features[column_name]
                .astype(str)
                .value_counts(normalize=True)
            )

            features[feature_name] = (
                features[column_name]
                .map(normalized_frequency)
                .fillna(0.0)
            )

        else:
            features[feature_name] = 0.0

    # ---------- Time Behaviour Features ----------

    if "Declaration_Time" in features.columns:
        declaration_hour = features["Declaration_Time"].dt.hour.fillna(0)
    else:
        declaration_hour = 0

    features["Off_Hours_Declaration"] = (
        (declaration_hour < 6) | (declaration_hour > 21)
    ).astype(int)

    # ---------- Weekend Declaration ----------

    if "Declaration_Date" in features.columns:
        features["Weekend_Declaration"] = (
            features["Declaration_Date"]
            .dt.dayofweek
            .fillna(0)
            .isin([5, 6])
        ).astype(int)
    else:
        features["Weekend_Declaration"] = 0

    return features