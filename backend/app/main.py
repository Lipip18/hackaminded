from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as risk_router

app = FastAPI(
	title="SmartContainer Risk Engine",
	version="1.0.0",
	description="AI/ML-based risk scoring and anomaly detection for container shipments",
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(risk_router)


@app.get("/")
def root() -> dict[str, str]:
	return {"message": "SmartContainer Risk Engine API is running."}
