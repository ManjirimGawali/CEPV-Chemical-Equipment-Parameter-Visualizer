import { useState, useEffect } from "react";
import api from "../api/client";
import Charts from "../components/Charts";
import CSVPreview from "../components/CSVPreview";
import { data } from "react-router-dom";
import Footer from "../components/Footer";
import CSVFormatExample from "../components/CSVFormatExample";
import TextInput from "../components/TextInput";
import Button from "../components/MyButton";
import sampleCsv from "../assets/file.csv?url";

export default function Dashboard() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(() => {
    const s = localStorage.getItem("dashboard_summary");
    if (!s || s === "undefined" || s === "null") return null;
    try {
      return JSON.parse(s);
    } catch {
      return null;
    }
  });
  const [fileName, setFileName] = useState(() => {
    const n = localStorage.getItem("dashboard_filename");
    if (!n || n === "undefined" || n === "null") return null;
    try {
      return JSON.parse(n);
    } catch {
      return null;
    }
  });
  const [datasetId, setDatasetId] = useState(() => {
    const id = localStorage.getItem("dashboard_datasetId");
    if (!id || id === "undefined" || id === "null") return null;
    try {
      return JSON.parse(id);
    } catch {
      return null;
    }
  });
  const [preview, setPreview] = useState(() => {
    const p = localStorage.getItem("dashboard_preview");
    if (!p || p === "undefined" || p === "null") return [];
    try {
      return JSON.parse(p);
    } catch {
      return [];
    }
  });
  const [datasetName, setDatasetName] = useState(() => {
    const n = localStorage.getItem("dashboard_datasetName");
    if (!n || n === "undefined" || n === "null") return null;
    try {
      return JSON.parse(n);
    } catch {
      return null;
    }
  });
  const [charts, setCharts] = useState(() => {
    const c = localStorage.getItem("dashboard_charts");
    if (!c || c === "undefined" || c === "null") return null;
    try {
      return JSON.parse(c);
    } catch {
      return null;
    }
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Sync state to localStorage
  useEffect(() => {
    if (summary)
      localStorage.setItem("dashboard_summary", JSON.stringify(summary));
    else localStorage.removeItem("dashboard_summary");
  }, [summary]);
  useEffect(() => {
    if (datasetId)
      localStorage.setItem("dashboard_datasetId", JSON.stringify(datasetId));
    else localStorage.removeItem("dashboard_datasetId");
  }, [datasetId]);
  useEffect(() => {
    if (preview && preview.length > 0)
      localStorage.setItem("dashboard_preview", JSON.stringify(preview));
    else localStorage.removeItem("dashboard_preview");
  }, [preview]);
  useEffect(() => {
    if (charts)
      localStorage.setItem("dashboard_charts", JSON.stringify(charts));
    else localStorage.removeItem("dashboard_charts");
  }, [charts]);

  useEffect(() => {
    if (fileName)
      localStorage.setItem("dashboard_filename", JSON.stringify(fileName));
    else localStorage.removeItem("dashboard_filename");
  }, [fileName]);

  useEffect(() => {
    if (datasetName)
      localStorage.setItem(
        "dashboard_datasetName",
        JSON.stringify(datasetName),
      );
    else localStorage.removeItem("dashboard_datasetName");
  }, [datasetName]);

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a CSV file");
      return;
    }

    if (!datasetName || datasetName.trim() === "") {
      setError("Please provide a dataset name");
      return;
    }

    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("name", datasetName);

    try {
      const res = await api.post("upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setFileName(res.filename);
      setSummary(res.data.summary);
      setDatasetId(res.data.dataset_id);
      setPreview(res.data.preview);
      setCharts(res.data.charts);

      localStorage.setItem("dashboard_filename", JSON.stringify(res.filename));
      alert("Upload successful");
    } catch (err) {
      setError(err.response?.data?.error || "Upload failed");
    } finally {
      setLoading(false);
    }
  };
  const handleDownloadSample = async () => {
    try {
      const response = await fetch(sampleCsv);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "sample.csv";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Failed to download sample CSV:", error);
      setError("Failed to download sample CSV");
    }
  };

  const downloadPDF = async () => {
    try {
      const res = await api.get(`report/${datasetId}/`, {
        responseType: "blob",
      });

      const blob = new Blob([res.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = `dataset_${datasetId}.pdf`;
      document.body.appendChild(a);
      a.click();

      a.remove();
      window.URL.revokeObjectURL(url);
    } catch {
      alert("Failed to download PDF");
    }
  };

  return (
    <div className="min-h-screen rounded-2xl bg-slate-50 px-6 py-10">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-4xl font-bold text-slate-900">Dashboard</h1>
          <p className="text-slate-600">
            Upload a CSV file to analyze and generate reports
          </p>
        </div>

        {/* Upload Card */}
        <div className="bg-white rounded-2xl shadow p-6 space-y-4">
          <h2 className="text-lg font-semibold text-slate-900">
            Upload CSV File
          </h2>
          
          

          <TextInput
            label="Dataset Name"
            value={datasetName}
            onChange={(e) => setDatasetName(e.target.value)}
            required
          />

          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
            className="block w-full text-sm text-slate-600
              file:mr-4 file:py-2 file:px-4
              file:rounded-lg file:border-0
              file:bg-slate-900 file:text-white
              hover:file:bg-slate-800"
            required
          />

          <button
            onClick={handleUpload}
            disabled={loading}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-slate-900 text-white rounded-lg font-semibold hover:bg-slate-800 disabled:bg-slate-400"
          >
            {loading ? "Uploading..." : "Upload & Analyze"}
          </button>
          <button
            onClick={handleDownloadSample}
            disabled={loading}
            className="inline-flex ml-4 items-center gap-2 px-5 py-2.5 bg-green-800 text-white rounded-lg font-semibold hover:bg-slate-800 disabled:bg-slate-400"
          >
            {loading ? "Downloading..." : "Download sample csv"}
          </button>

          {error && <p className="text-sm text-red-600 font-medium">{error}</p>}
          <CSVFormatExample />
        </div>

        {/* Summary */}
        {summary && (
          <div className="bg-white rounded-2xl shadow p-6 space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-slate-900">
                Dataset Summary of {datasetName}
              </h2>
              <button
                onClick={downloadPDF}
                className="px-4 py-2 bg-slate-900 text-white rounded-lg hover:bg-slate-800"
              >
                Download PDF
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
              <Stat
                label="Total Equipment"
                value={summary.total_equipment.toString()}
              />
              <Stat
                label="Avg Flowrate"
                value={summary.average_flowrate.toFixed(3)}
              />
              <Stat
                label="Avg Pressure"
                value={summary.average_pressure.toFixed(3)}
              />
              <Stat
                label="Avg Temperature"
                value={summary.average_temperature.toFixed(3)}
              />
            </div>

            <div>
              <h3 className="font-semibold text-slate-900 mb-2">
                Type Distribution
              </h3>
              <ul className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-sm">
                {Object.entries(summary.type_distribution).map(
                  ([type, count]) => (
                    <li
                      key={type}
                      className="bg-slate-100 rounded-lg px-3 py-2"
                    >
                      {type}: <strong>{count}</strong>
                    </li>
                  ),
                )}
              </ul>
            </div>
          </div>
        )}

        {/* Charts */}
        {charts && (
          <div className="bg-white rounded-2xl shadow p-6">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">
              Analytics
            </h2>
            <Charts charts={charts} />
          </div>
        )}

        {/* CSV Preview */}
        {preview.length > 0 && (
          <div className="bg-white rounded-2xl shadow p-6">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">
              CSV Preview (First 10 Rows)
            </h2>
            <CSVPreview rows={preview} />
          </div>
        )}
      </div>
    </div>
  );
}

/* Small stat card */
function Stat({ label, value }) {
  return (
    <div className="bg-slate-100 rounded-xl p-4">
      <p className="text-sm text-slate-600">{label}</p>
      <p className="text-xl font-bold text-slate-900">{value}</p>
    </div>
  );
}
