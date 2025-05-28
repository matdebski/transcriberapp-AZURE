import React, { useState } from 'react';
import axios from 'axios';

const allowedExtensions = [".wav", ".mp3", ".mp4", ".m4a", ".webm", ".ogg"];

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;

    const ext = selected.name.slice(((selected.name.lastIndexOf(".") - 1) >>> 0) + 2).toLowerCase();
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
      await axios.post(
        "https://upload-transcriber.azurewebsites.net/api/upload", // <- Twój backend
        form
      );
      setStatus("Uploaded and queued for processing");
    } catch (err) {
      setStatus("Upload failed");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Transcriber</h1>
      <input type="file" onChange={handleChange} />
      <button onClick={handleUpload} disabled={!file}>Upload</button>
      <p>{status}</p>
    </div>
  );
}

export default App;