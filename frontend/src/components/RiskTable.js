import React from "react";

function RiskTable({ rows }) {
	if (!rows?.length) {
		return null;
	}

	const sortedRows = [...rows].sort((first, second) => {
		return Number(second.Risk_Score) - Number(first.Risk_Score);
	});

	return (
		<section className="card">
			<h2>Container Predictions</h2>
			<p className="muted">Ranked by risk score (highest first).</p>
			<div className="table-wrapper">
				<table>
					<thead>
						<tr>
							<th>#</th>
							<th>Container ID</th>
							<th>Risk Score</th>
							<th>Risk Level</th>
							<th>Explanation</th>
						</tr>
					</thead>
					<tbody>
						{sortedRows.map((row, index) => (
							<tr key={row.Container_ID}>
								<td>{index + 1}</td>
								<td>{row.Container_ID}</td>
								<td>{Number(row.Risk_Score).toFixed(4)}</td>
								<td>
									<span
										className={`badge ${
											row.Risk_Level === "Critical" ? "badge-critical" : "badge-low"
										}`}
									>
										{row.Risk_Level}
									</span>
								</td>
								<td>{row.Explanation_Summary}</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</section>
	);
}

export default RiskTable;
