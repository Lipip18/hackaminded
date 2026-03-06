import React from "react";

function RiskChart({ summary }) {
	if (!summary) {
		return null;
	}

	const total = summary.total_containers || 1;
	const criticalPercent = ((summary.critical_count / total) * 100).toFixed(1);
	const lowPercent = ((summary.low_risk_count / total) * 100).toFixed(1);

	return (
		<section className="card">
			<h2>Risk Distribution</h2>
			<p className="muted">Visual split of prioritization outcomes across the uploaded batch.</p>

			<div className="bar-row">
				<span>Critical ({summary.critical_count})</span>
				<div className="bar-track">
					<div className="bar-fill critical" style={{ width: `${criticalPercent}%` }} />
				</div>
				<strong>{criticalPercent}%</strong>
			</div>

			<div className="bar-row">
				<span>Low Risk ({summary.low_risk_count})</span>
				<div className="bar-track">
					<div className="bar-fill low" style={{ width: `${lowPercent}%` }} />
				</div>
				<strong>{lowPercent}%</strong>
			</div>
		</section>
	);
}

export default RiskChart;
