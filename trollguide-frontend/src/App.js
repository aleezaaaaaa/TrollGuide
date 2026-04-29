import React, { useState, useEffect } from "react";
import Dashboard from "./Dashboard";
import AdminPanel from "./AdminPanel";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useNavigate
} from "react-router-dom";

// ================= STYLES =================
const styles = {
  page: {
    background: "#000",
    color: "#fff",
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    fontFamily: "Segoe UI, sans-serif"
  },
  title: {
    color: "#FFD700",
    fontSize: "42px",
    marginBottom: "5px"
  },
  subtitle: {
    color: "#aaa",
    marginBottom: "30px"
  },
  card: {
    background: "#111",
    padding: "25px",
    borderRadius: "15px",
    width: "500px",
    boxShadow: "0 0 20px rgba(255, 215, 0, 0.2)"
  },
  textarea: {
    width: "100%",
    height: "120px",
    padding: "12px",
    borderRadius: "10px",
    border: "1px solid #333",
    background: "#000",
    color: "#fff",
    marginBottom: "20px"
  },
  actions: {
    display: "flex",
    gap: "10px",
    flexWrap: "wrap"
  },
  primaryBtn: {
    flex: 1,
    padding: "10px",
    background: "#FFD700",
    border: "none",
    borderRadius: "8px",
    fontWeight: "bold",
    cursor: "pointer"
  },
  secondaryBtn: {
    flex: 1,
    padding: "10px",
    background: "#333",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer"
  },
  fileInput: {
    flex: 1,
    padding: "10px",
    background: "#222",
    borderRadius: "8px",
    textAlign: "center",
    cursor: "pointer"
  }
};

// ================= HOME =================
function Home() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [imageFile, setImageFile] = useState(null);
  const [preview, setPreview] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    console.log("UPDATED RESULT:", result);
  }, [result]);

  // ================= TEXT =================
  const analyze = async () => {
    if (!text) return alert("Enter text");

    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });

      const data = await res.json();
      setResult(data);
    } catch {
      alert("Backend error");
    }
    setLoading(false);
  };

  // ================= IMAGE INPUT HANDLER (FIXED) =================
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setImageFile(file);

    if (file) {
      setPreview(URL.createObjectURL(file));
    }
  };

  // ================= IMAGE UPLOAD =================
  const handleImageUpload = async () => {
    if (!imageFile) return alert("Upload image");

    const formData = new FormData();
    formData.append("file", imageFile);

    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/image", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Image processing failed. Check backend.");
    }
    setLoading(false);
  };

  // ================= DOWNLOAD PDF =================
  const downloadReport = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(result)
      });

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "report.pdf";
      a.click();
    } catch {
      alert("PDF failed");
    }
  };

  return (
    <div style={styles.page}>
      <h1 style={styles.title}>🛡 TrollGuide</h1>
      <p style={styles.subtitle}>
        Detect cyberbullying & get legal guidance instantly
      </p>

      <div style={styles.card}>
        <textarea
          placeholder="Enter text..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          style={styles.textarea}
        />

        <div style={styles.actions}>
          <button onClick={analyze} style={styles.primaryBtn}>
            {loading ? "Analyzing..." : "🚀 Analyze"}
          </button>

          {/* ✅ FIXED INPUT */}
          <label style={styles.fileInput}>
            Upload Image
            <input
              type="file"
              hidden
              onChange={handleFileChange}
            />
          </label>

          <button onClick={handleImageUpload} style={styles.secondaryBtn}>
            Analyze Image
          </button>
        </div>

        {/* ✅ IMAGE PREVIEW */}
        {preview && (
          <div style={{ marginTop: "20px", textAlign: "center" }}>
            <p style={{ color: "#aaa" }}>Uploaded Image:</p>
            <img
              src={preview}
              alt="preview"
              style={{
                maxWidth: "100%",
                maxHeight: "250px",
                borderRadius: "10px",
                border: "1px solid #333"
              }}
            />
          </div>
        )}
      </div>

      {/* ================= RESULT ================= */}
      {result && (
        <div
          style={{
            marginTop: "30px",
            textAlign: "center",
            background: "#111",
            padding: "20px",
            borderRadius: "12px",
            boxShadow: "0 0 15px rgba(255,215,0,0.2)"
          }}
        >
          <h2
            style={{
              color: result.label === "Toxic" ? "#ff4d4d" : "#00C49F"
            }}
          >
            {result.label === "Toxic" ? "⚠️ Toxic" : "✅ Safe"}
          </h2>

          <p>
            Confidence:{" "}
            {result.confidence !== undefined && result.confidence !== null
              ? `${(result.confidence * 100).toFixed(2)}%`
              : "N/A"}
          </p>

          {result.legal && (
            <div style={{ marginTop: "15px" }}>
              <h3>⚖️ Legal Guidance</h3>
              <p><b>{result.legal.crime}</b></p>
              <p>{result.legal.law}</p>

              <ul>
                {result.legal.actions.map((a, i) => (
                  <li key={i}>{a}</li>
                ))}
              </ul>

              <a
                href="https://cybercrime.gov.in/"
                target="_blank"
                rel="noreferrer"
              >
                <button
                  style={{
                    marginTop: "10px",
                    padding: "10px",
                    background: "#ff4d4d",
                    color: "#fff",
                    border: "none",
                    borderRadius: "6px",
                    cursor: "pointer"
                  }}
                >
                  🚨 Report Crime
                </button>
              </a>
            </div>
          )}

          <button onClick={downloadReport} style={styles.primaryBtn}>
            📄 Download Report
          </button>

          <div style={{ marginTop: "10px" }}>
            <button onClick={() => navigate("/dashboard")} style={styles.secondaryBtn}>
              📊 Dashboard
            </button>

            <button onClick={() => navigate("/admin")} style={styles.secondaryBtn}>
              🛠 Admin
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

// ================= ROUTER =================
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/admin" element={<AdminPanel />} />
      </Routes>
    </Router>
  );
}

export default App;