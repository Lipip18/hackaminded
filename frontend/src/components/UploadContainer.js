import React, { useState } from "react";

function UploadContainer({ onSubmit, onRunDemo, onRunPresetDemo, loading, demoLoading }) {
	const [selectedFile, setSelectedFile] = useState(null);

	const handleFileChange = (event) => {
		const file = event.target.files?.[0] || null;
		setSelectedFile(file);
	};

	const handleSubmit = async (event) => {
		event.preventDefault();
		if (!selectedFile || loading) {
			return;
		}
		onSubmit(selectedFile);
	};

	return (
		<section className="card upload-card">
			<h2>Batch Upload</h2>
			<p className="muted">Upload container shipment data in CSV or Excel format.</p>
			<form onSubmit={handleSubmit} className="upload-form">
				<input
					type="file"
					accept=".csv,.xlsx,.xls"
					onChange={handleFileChange}
					disabled={loading}
				/>
				<button type="submit" disabled={!selectedFile || loading}>
					{loading ? "Processing..." : "Run Risk Assessment"}
				</button>
				<button type="button" className="secondary" onClick={onRunDemo} disabled={loading || demoLoading}>
					{demoLoading ? "Loading Demo..." : "Load Demo Dataset"}
				</button>
			</form>
			<div className="preset-actions">
				<button
					type="button"
					className="secondary"
					onClick={() => onRunPresetDemo("low-risk")}
					disabled={loading || demoLoading}
				>
					Load Low-Risk Scenario
				</button>
				<button
					type="button"
					className="secondary"
					onClick={() => onRunPresetDemo("critical-heavy")}
					disabled={loading || demoLoading}
				>
					Load Critical-Heavy Scenario
				</button>
			</div>
			{selectedFile && (
				<div className="file-meta">
					<small>
						Selected: <strong>{selectedFile.name}</strong>
					</small>
					<small>{Math.max(1, Math.round(selectedFile.size / 1024))} KB</small>
				</div>
			)}
			<p className="hint">
				Required columns must include container, value/weight, route, and clearance details.
			</p>
		</section>
	);
}

export default UploadContainer;
