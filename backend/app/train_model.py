import pandas as pd

from app.services.feature_engineering import build_features
from app.services.risk_model import train_model

# Correct dataset path
df = pd.read_csv("app/data/Historical Data.csv")

# Build features
features = build_features(df)

# Train model
train_model(features)

print("Model trained successfully and saved.")