from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import HTTPException, UploadFile

from app.config import settings


def ensure_required_columns(dataframe: pd.DataFrame) -> None:
	missing_columns = [
		column for column in settings.required_columns if column not in dataframe.columns
	]
	if missing_columns:
		raise HTTPException(
			status_code=400,
			detail=f"Missing required columns: {', '.join(missing_columns)}",
		)


def load_upload_to_dataframe(file: UploadFile) -> pd.DataFrame:
	suffix = Path(file.filename or "").suffix.lower()
	file_bytes = file.file.read()

	if suffix == ".csv":
		dataframe = pd.read_csv(BytesIO(file_bytes))
	elif suffix in {".xlsx", ".xls"}:
		dataframe = pd.read_excel(BytesIO(file_bytes))
	else:
		raise HTTPException(
			status_code=400,
			detail="Only CSV and Excel files are supported.",
		)

	if dataframe.empty:
		raise HTTPException(status_code=400, detail="Uploaded file is empty.")

	ensure_required_columns(dataframe)
	return dataframe


def make_output_dir() -> Path:
	settings.output_dir.mkdir(parents=True, exist_ok=True)
	return settings.output_dir


def to_native(value):
	if isinstance(value, (np.floating, np.float32, np.float64)):
		return float(value)
	if isinstance(value, (np.integer, np.int32, np.int64)):
		return int(value)
	if pd.isna(value):
		return None
	return value
