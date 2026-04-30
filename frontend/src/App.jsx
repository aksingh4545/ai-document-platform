import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
const API = import.meta.env.VITE_API_URL;

function App() {
  const [stats, setStats] = useState(null);
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const res = await axios.get("${API}/api/dashboard");
      setStats(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleUpload = async () => {
    if (!file) return alert("Select a file");

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post("${API}/api/upload", formData);
      const docId = res.data.id;

      await axios.post(`${API}/api/process/${docId}`);
      await axios.post(`${API}/api/embed/${docId}`);

      alert("Document ready!");
      fetchDashboard();
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }

    setLoading(false);
  };

  const askQuestion = async () => {
    if (!query) return;

    setLoading(true);

    try {
      const res = await axios.post(`${API}/api/ask?query=${query}`);
      setAnswer(res.data.answer);
      fetchDashboard();
    } catch (err) {
      console.error(err);
      alert("Error asking question");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1 className="title">AI Document Assistant</h1>

      {/* Dashboard */}
      <div className="card">
        <h2>Dashboard</h2>
        {stats ? (
          <div className="dashboard">
            <div className="stat">
              <p>Total Documents</p>
              <h3>{stats.total_documents}</h3>
            </div>
            <div className="stat">
              <p>Total Chunks</p>
              <h3>{stats.total_chunks}</h3>
            </div>
            <div className="stat">
              <p>Total Queries</p>
              <h3>{stats.total_queries}</h3>
            </div>
          </div>
        ) : (
          <p>Loading...</p>
        )}
      </div>

      {/* Upload */}
      <div className="card">
        <h3>Upload Document</h3>
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button onClick={handleUpload}>Upload & Process</button>
      </div>

      {/* Ask */}
      <div className="card">
        <h3>Ask Question</h3>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask something..."
        />
        <button onClick={askQuestion}>Ask</button>

        {loading && <p>Processing...</p>}

        <div className="answer">
          <h4>Answer:</h4>
          <p>{answer}</p>
        </div>
      </div>
    </div>
  );
}

export default App;
