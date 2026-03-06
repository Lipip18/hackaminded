from pathlib import Path


class Settings:
	critical_threshold: float = 0.65
	weight_diff_pct_threshold: float = 15.0
	dwell_time_threshold_hours: float = 96.0
	anomaly_score_weight: float = 0.45
	output_dir: Path = Path(__file__).resolve().parent / "data" / "outputs"

	required_columns = [
		"Container_ID",
		"Declaration_Date",
		"Declaration_Time",
		"Trade_Regime",
		"Origin_Country",
		"Destination_Country",
		"Destination_Port",
		"HS_Code",
		"Importer_ID",
		"Exporter_ID",
		"Declared_Value",
		"Declared_Weight",
		"Measured_Weight",
		"Shipping_Line",
		"Dwell_Time_Hours",
		"Clearance_Status",
	]


settings = Settings()
