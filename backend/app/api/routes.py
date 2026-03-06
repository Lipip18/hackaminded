from pathlib import Path
from uuid import uuid4

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.models.container_schema import BatchPredictionResponse
from app.services.anomaly_detector import detect_anomalies
from app.services.explainability import generate_explanations
from app.services.feature_engineering import build_features
from app.services.risk_model import predict_risk
from app.utils.helpers import ensure_required_columns, load_upload_to_dataframe, make_output_dir, to_native

router = APIRouter(prefix="/api", tags=["Risk Engine"])

job_registry: dict[str, dict] = {}

DEFAULT_DATASET_PATH = Path("backend/data/historical_data.csv")

DEMO_DATASET_MAP = {
	"sample": ("backend", "app", "data", "sample_data.csv"),
	"low-risk": ("test_data", "test_low_risk.csv"),
	"critical-heavy": ("test_data", "test_critical_cases.csv"),
	"mixed": ("test_data", "test_mixed_batch.csv"),
}


def _run_prediction_pipeline(dataframe: pd.DataFrame) -> dict:
	features = build_features(dataframe)

	anomaly_score, anomaly_flags = detect_anomalies(features)
	risk_score, risk_level, score_components = predict_risk(features, anomaly_score)

	explanations = generate_explanations(
		features=features,
		anomaly_flags=anomaly_flags,
		score_components=score_components,
		risk_level=risk_level,
	)

	container_id = dataframe["Container_ID"].astype(str)

	prediction_frame = pd.DataFrame(
		{
			"Container_ID": container_id,
			"Risk_Score": risk_score,
			"Risk_Level": risk_level,
			"Explanation_Summary": explanations,
		}
	)

	total_count = len(prediction_frame)
	critical_count = int((prediction_frame["Risk_Level"] == "Critical").sum())
	low_risk_count = int((prediction_frame["Risk_Level"] == "Low Risk").sum())

	summary = {
		"total_containers": total_count,
		"critical_count": critical_count,
		"low_risk_count": low_risk_count,
	}

	job_id = uuid4().hex[:12]
	output_dir = make_output_dir()
	output_file_path = output_dir / f"predictions_{job_id}.csv"

	prediction_frame.to_csv(output_file_path, index=False)

	preview = prediction_frame.head(200).to_dict(orient="records")
	preview = [{key: to_native(value) for key, value in row.items()} for row in preview]

	job_registry[job_id] = {
		"summary": summary,
		"output_file": str(output_file_path),
		"preview": preview,
	}

	return {
		"job_id": job_id,
		"summary": summary,
		"predictions_preview": preview,
	}


def _load_demo_dataframe(preset: str) -> pd.DataFrame:
	key = preset.strip().lower()

	if key not in DEMO_DATASET_MAP:
		allowed = ", ".join(DEMO_DATASET_MAP.keys())
		raise HTTPException(status_code=400, detail=f"Invalid preset '{preset}'. Allowed: {allowed}")

	backend_root = Path(__file__).resolve().parents[2]
	project_root = backend_root.parent

	path_parts = DEMO_DATASET_MAP[key]

	if path_parts[0] == "backend":
		dataset_path = project_root / path_parts[0] / path_parts[1] / path_parts[2] / path_parts[3]
	else:
		dataset_path = project_root / path_parts[0] / path_parts[1]

	if not dataset_path.exists():
		raise HTTPException(status_code=404, detail=f"Demo dataset not found: {dataset_path.name}")

	dataframe = pd.read_csv(dataset_path)

	ensure_required_columns(dataframe)

	return dataframe


def _load_default_training_dataset() -> pd.DataFrame:

	if not DEFAULT_DATASET_PATH.exists():
		raise HTTPException(status_code=404, detail="Default training dataset not found")

	dataframe = pd.read_csv(DEFAULT_DATASET_PATH)

	ensure_required_columns(dataframe)

	return dataframe


@router.get("/health")
def health_check() -> dict[str, str]:
	return {"status": "ok"}


@router.post("/predict/batch", response_model=BatchPredictionResponse)
def predict_batch(file: UploadFile = File(...)) -> dict:

	dataframe = load_upload_to_dataframe(file)

	return _run_prediction_pipeline(dataframe)


@router.post("/predict/train-default", response_model=BatchPredictionResponse)
def train_default_dataset() -> dict:

	dataframe = _load_default_training_dataset()

	return _run_prediction_pipeline(dataframe)


@router.post("/predict/demo", response_model=BatchPredictionResponse)
def predict_demo() -> dict:

	dataframe = _load_demo_dataframe("sample")

	return _run_prediction_pipeline(dataframe)


@router.post("/predict/demo/{preset}", response_model=BatchPredictionResponse)
def predict_demo_preset(preset: str) -> dict:

	dataframe = _load_demo_dataframe(preset)

	return _run_prediction_pipeline(dataframe)


@router.get("/summary/{job_id}")
def get_summary(job_id: str) -> dict:

	job_data = job_registry.get(job_id)

	if not job_data:
		raise HTTPException(status_code=404, detail="Job not found")

	return {"job_id": job_id, "summary": job_data["summary"]}


@router.get("/predictions/{job_id}.csv")
def download_prediction_file(job_id: str) -> FileResponse:

	job_data = job_registry.get(job_id)

	if not job_data:
		raise HTTPException(status_code=404, detail="Job not found")

	file_path = Path(job_data["output_file"])

	if not file_path.exists():
		raise HTTPException(status_code=404, detail="Prediction file not found")

	return FileResponse(
		path=str(file_path),
		filename=f"predictions_{job_id}.csv",
		media_type="text/csv",
	)