import pandas as pd


def _build_reason(row: pd.Series, flags: pd.Series, components: pd.Series) -> str:
	reasons = []

	if flags["weight_flag"]:
		reasons.append("large declared vs measured weight difference")
	if flags["value_flag"]:
		reasons.append("unusual value-to-weight ratio")
	if flags["dwell_flag"]:
		reasons.append("extended dwell time at port")
	if flags["behavior_flag"]:
		reasons.append("irregular importer/exporter or route behavior")
	if flags["model_flag"]:
		reasons.append("overall profile differs from typical shipments")

	if not reasons:
		top_component = components.sort_values(ascending=False).index[0]
		mapped = {
			"anomaly_component": "minor anomaly signal",
			"weight_component": "small weight mismatch",
			"value_component": "slight value-to-weight deviation",
			"dwell_component": "moderately high dwell time",
			"off_hours_component": "declared during off-hours",
			"weekend_component": "declared on a weekend",
		}
		reasons.append(mapped.get(top_component, "normal shipment profile"))

	lead_reasons = ", ".join(reasons[:2])
	return f"Risk driven by {lead_reasons}. Review recommended based on combined anomaly indicators."


def generate_explanations(
	features: pd.DataFrame,
	anomaly_flags: pd.DataFrame,
	score_components: pd.DataFrame,
	risk_level: pd.Series,
) -> pd.Series:
	explanations = []
	for index in features.index:
		explanation = _build_reason(
			features.loc[index],
			anomaly_flags.loc[index],
			score_components.loc[index],
		)
		if risk_level.loc[index] == "Low Risk":
			explanation = (
				"Risk remains low: shipment pattern is largely consistent with expected trade behavior."
			)
			if anomaly_flags.loc[index].any():
				explanation = (
					"Low risk with minor irregularities; monitor weight/value consistency for confirmation."
				)
		explanations.append(explanation)
	return pd.Series(explanations, index=features.index)
