from pydantic import BaseModel


class PredictionRow(BaseModel):
	Container_ID: str
	Risk_Score: float
	Risk_Level: str
	Explanation_Summary: str


class BatchSummary(BaseModel):
	total_containers: int
	critical_count: int
	low_risk_count: int


class BatchPredictionResponse(BaseModel):
	job_id: str
	summary: BatchSummary
	predictions_preview: list[PredictionRow]
