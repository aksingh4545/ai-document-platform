import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const API = import.meta.env.VITE_API_URL;
const apiClient = axios.create({
  baseURL: API,
  headers: {
    "ngrok-skip-browser-warning": "true",
  },
});

function App() {
  const [stats, setStats] = useState(null);
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    const res = await apiClient.get("/dashboard");
    setStats(res.data);
  };

  const handleUpload = async () => {
    if (!file) return alert("Select a file");

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    const res = await apiClient.post("/upload", formData);
    const docId = res.data.id;

    await apiClient.post(`/process/${docId}`);
    await apiClient.post(`/embed/${docId}`);

    alert("Document ready!");
    fetchDashboard();

    setLoading(false);
  };

  const askQuestion = async () => {
    const res = await apiClient.post(`/ask?query=${query}`);
    setAnswer(res.data.answer);
    setHistory((prev) => [
      {
        question: query,
        answer: res.data.answer,
      },
      ...prev,
    ]);
  };

  return (
    <div>
      <h1>AI Document Assistant</h1>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={askQuestion}>Ask</button>

      <p>{answer}</p>

      {history.length > 0 && (
        <div>
          <h2>Query History</h2>
          {history.map((item, index) => (
            <div key={`${item.question}-${index}`}>
              <p><strong>Q:</strong> {item.question}</p>
              <p><strong>A:</strong> {item.answer}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;