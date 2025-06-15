import React, { useState } from 'react';
import axios from 'axios';

const allowedExtensions = [".wav", ".mp3", ".mp4", ".m4a", ".webm", ".ogg"];
const API_URL = process.env.REACT_APP_API_URL;
const BLOB_STORAGE_URL = "https://storage0transcriber.blob.core.windows.net/output-transcriber";
console.log(API_URL)

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [result, setResult] = useState("");


  const handleChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;

    const ext = selected.name.split(".").pop().toLowerCase();
    if (!allowedExtensions.includes("." + ext)) {
      setStatus("Invalid file type. Only audio/video formats are allowed.");
      return;
    }

    setFile(selected);
    setStatus("");
  };

  const handleUpload = async () => {
    if (!file) return;
    const form = new FormData();
    form.append("file", file);
    setStatus("Uploading...");
    try {
      const res = await axios.post(API_URL, form);
      const fileId = res.data.file_id;
      setStatus("File uploaded. Processing...");
      checkResult(fileId);
    } catch (err) {
      const errorMsg = err.response?.data?.message || "Upload failed";
      setStatus(errorMsg);
    }
  };

  const checkResult = async (fileId) => {
    const url = `${BLOB_STORAGE_URL}/${fileId}`;
    console.log("Checking result...")
    console.log(url);
    const interval = setInterval(async () => {
      try {
        const response = await fetch(url);
        if (response.ok) {
          const text = await response.text();
          setResult(text);
          setStatus("Processing complete");
          clearInterval(interval);
        }
      } catch (e) {
        // still processing
      }
    }, 3000);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Transcriber</h1>
      <input type="file" onChange={handleChange} />
      <button onClick={handleUpload} disabled={!file}>Upload</button>
      <p>{status}</p>
      {result && <div><h2>Result:</h2><p>{result}</p></div>}
    </div>
  );
}

export default App;