import React from "react";
import RiskChart from "./RiskChart";
import RiskTable from "./RiskTable";

function Dashboard({ summary, predictions }) {
	if (!summary) {
		return (
			<section className="card empty-state">
				<h2>Ready for Demo</h2>
				<p>
					Upload a batch file to generate risk scores, anomaly-driven categorization, and
					explanation summaries.
				</p>
			</section>
		);
	}

	const criticalPct = ((summary.critical_count / Math.max(1, summary.total_containers)) * 100).toFixed(1);
	const lowPct = ((summary.low_risk_count / Math.max(1, summary.total_containers)) * 100).toFixed(1);

	return (
		<div className="dashboard-grid">
			<section className="card stats-card">
				<h2>Operational Summary</h2>
				<div className="stats-grid">
					<div className="stat-block">
						<p>Total Processed</p>
						<strong>{summary.total_containers}</strong>
					</div>
					<div className="stat-block critical">
						<p>Critical</p>
						<strong>{summary.critical_count}</strong>
						<small>{criticalPct}% of batch</small>
					</div>
					<div className="stat-block low">
						<p>Low Risk</p>
						<strong>{summary.low_risk_count}</strong>
						<small>{lowPct}% of batch</small>
					</div>
				</div>
			</section>

			<RiskChart summary={summary} />
			<RiskTable rows={predictions} />
		</div>
	);
}

export default Dashboard;
