import joblib

model = joblib.load("app/models/risk_model.pkl")

print(model)