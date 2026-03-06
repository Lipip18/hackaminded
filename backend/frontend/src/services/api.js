import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

const apiClient = axios.create({
	baseURL: API_BASE_URL,
	timeout: 60000,
});

export async function uploadAndPredict(file) {
	const formData = new FormData();
	formData.append("file", file);

	const response = await apiClient.post("/predict/batch", formData, {
		headers: { "Content-Type": "multipart/form-data" },
	});
	return response.data;
}

export async function runDemoPrediction() {
	const response = await apiClient.post("/predict/demo");
	return response.data;
}

export async function runPresetDemoPrediction(preset) {
	const response = await apiClient.post(`/predict/demo/${preset}`);
	return response.data;
}

export async function fetchSummary(jobId) {
	const response = await apiClient.get(`/summary/${jobId}`);
	return response.data;
}

export function buildDownloadUrl(jobId) {
	return `${API_BASE_URL}/predictions/${jobId}.csv`;
}
