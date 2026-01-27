const API_URL = "http://127.0.0.1:8000"; // FastAPI backend

async function fetchData(endpoint) {
    const res = await fetch(`${API_URL}${endpoint}`);
    if (!res.ok) throw new Error("Failed to fetch");
    return await res.json();
}
