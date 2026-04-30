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
    const res = await axios.get(`${API}/dashboard`);
    setStats(res.data);
  };

  const handleUpload = async () => {
    if (!file) return alert("Select a file");

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(`${API}/upload`, formData);
    const docId = res.data.id;

    await axios.post(`${API}/process/${docId}`);
    await axios.post(`${API}/embed/${docId}`);

    alert("Document ready!");
    fetchDashboard();

    setLoading(false);
  };

  const askQuestion = async () => {
    const res = await axios.post(`${API}/ask?query=${query}`);
    setAnswer(res.data.answer);
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
    </div>
  );
}

export default App;