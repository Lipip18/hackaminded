import React, { useState } from "react";
import Dashboard from "./components/Dashboard";
import UploadContainer from "./components/UploadContainer";
import {
	buildDownloadUrl,
	runDemoPrediction,
	runPresetDemoPrediction,
	uploadAndPredict,
} from "./services/api";
import "./styles/dashboard.css";

function App() {
	const [loading, setLoading] = useState(false);
	const [demoLoading, setDemoLoading] = useState(false);
	const [error, setError] = useState("");
	const [summary, setSummary] = useState(null);
	const [predictions, setPredictions] = useState([]);
	const [jobId, setJobId] = useState("");
	const [lastRunAt, setLastRunAt] = useState("");

	const handleUpload = async (file) => {
		setLoading(true);
		setError("");

		try {
			const response = await uploadAndPredict(file);
			setSummary(response.summary);
			setPredictions(response.predictions_preview || []);
			setJobId(response.job_id || "");
			setLastRunAt(new Date().toLocaleString());
		} catch (uploadError) {
			const detail =
				uploadError?.response?.data?.detail ||
				"Failed to process file. Verify file format and required columns.";
			setError(detail);
		} finally {
			setLoading(false);
		}
	};

	const handleRunDemo = async () => {
		setDemoLoading(true);
		setError("");

		try {
			const response = await runDemoPrediction();
			setSummary(response.summary);
			setPredictions(response.predictions_preview || []);
			setJobId(response.job_id || "");
			setLastRunAt(new Date().toLocaleString());
		} catch (demoError) {
			const detail =
				demoError?.response?.data?.detail ||
				"Failed to load demo dataset from backend.";
			setError(detail);
		} finally {
			setDemoLoading(false);
		}
	};

	const handleRunPresetDemo = async (preset) => {
		setDemoLoading(true);
		setError("");

		try {
			const response = await runPresetDemoPrediction(preset);
			setSummary(response.summary);
			setPredictions(response.predictions_preview || []);
			setJobId(response.job_id || "");
			setLastRunAt(new Date().toLocaleString());
		} catch (demoError) {
			const detail =
				demoError?.response?.data?.detail ||
				"Failed to load preset demo dataset.";
			setError(detail);
		} finally {
			setDemoLoading(false);
		}
	};

	return (
		<main className="app-shell">
			<header className="app-header">
				<div>
					<p className="eyebrow">Hackathon Demo</p>
					<h1>SmartContainer Risk Engine</h1>
					<p>
						AI-assisted anomaly detection and risk prioritization for container shipments.
					</p>
				</div>
				<div className="status-chip">Live Analysis Mode</div>
			</header>

			<UploadContainer
				onSubmit={handleUpload}
				onRunDemo={handleRunDemo}
				onRunPresetDemo={handleRunPresetDemo}
				loading={loading}
				demoLoading={demoLoading}
			/>

			{error && <section className="card error-card">{error}</section>}

			{jobId && (
				<section className="card result-card">
					<div>
						<p className="muted">Batch Job ID</p>
						<strong>{jobId}</strong>
						{lastRunAt && <p className="muted">Last run: {lastRunAt}</p>}
					</div>
					<div className="result-actions">
						<a href={buildDownloadUrl(jobId)} target="_blank" rel="noreferrer">
							Download Prediction CSV
						</a>
					</div>
				</section>
			)}

			<Dashboard summary={summary} predictions={predictions} />
		</main>
	);
}

export default App;
