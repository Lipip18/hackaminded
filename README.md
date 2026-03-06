# SmartContainer Risk Engine

AI/ML-based container shipment risk assessment system for anomaly detection, risk scoring, and explainable inspection prioritization.

## What This Project Delivers

- Batch processing of structured container shipment data (CSV/Excel)
- Risk score prediction for each container
- Risk categorization into:
	- `Critical`
	- `Low Risk`
- Basic anomaly detection for:
	- Weight mismatch
	- Value-to-weight irregularities
	- Dwell-time irregularities
	- Behavioral irregularities (route/trader frequency)
- Explainability summary (1-2 lines) for each prediction
- Dashboard/report-style frontend with totals and distribution

## Project Structure

```text
backend/
	requirements.txt
	run.py
	app/
		main.py
		config.py
		api/routes.py
		data/sample_data.csv
		models/container_schema.py
		services/
			feature_engineering.py
			anomaly_detector.py
			risk_model.py
			explainability.py
		utils/helpers.py

frontend/
	package.json
	public/index.html
	src/
		index.js
		App.js
		components/
			UploadContainer.js
			Dashboard.js
			RiskChart.js
			RiskTable.js
		services/api.js
		styles/dashboard.css
```

## Backend Workflow

1. Upload CSV/Excel
2. Validate required schema
3. Build engineered features
4. Run anomaly detection (rules + isolation forest signal)
5. Compute hybrid risk score
6. Assign risk level (`Critical` / `Low Risk`)
7. Generate explanation summary
8. Return preview + save downloadable predictions CSV

## API Endpoints

- `GET /` - service status
- `GET /api/health` - health check
- `POST /api/predict/batch` - upload data and run predictions
- `GET /api/summary/{job_id}` - summary metrics for batch
- `GET /api/predictions/{job_id}.csv` - download prediction output CSV

## Required Input Columns

- `Container_ID`
- `Declaration_Date`
- `Declaration_Time`
- `Trade_Regime`
- `Origin_Country`
- `Destination_Country`
- `Destination_Port`
- `HS_Code`
- `Importer_ID`
- `Exporter_ID`
- `Declared_Value`
- `Declared_Weight`
- `Measured_Weight`
- `Shipping_Line`
- `Dwell_Time_Hours`
- `Clearance_Status`

## Output Fields

- `Container_ID`
- `Risk_Score` (0-1)
- `Risk_Level` (`Critical`/`Low Risk`)
- `Explanation_Summary`

## Run Instructions

### 1) Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Backend runs on `http://localhost:8000`.

### 2) Frontend

```powershell
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000` and connects to backend `http://localhost:8000/api`.

## Demo Steps

1. Start backend and frontend
2. Upload `backend/app/data/sample_data.csv`
3. Review summary cards and risk distribution
4. Inspect per-container explanation lines
5. Download prediction CSV

## Notes

- This implementation is designed for hackathon practicality: simple, explainable, and modular.
- Risk thresholds are configurable in `backend/app/config.py`.
- For production, add persistent job storage, authentication, and model retraining pipeline.
