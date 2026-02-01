import { useEffect, useState, useRef } from "react";
import api from "../api/client";
import Charts from "../components/Charts";
import CSVPreview from "../components/CSVPreview";

export default function History() {
  const analysisRef = useRef(null);

  const [datasets, setDatasets] = useState(() => {
    const d = localStorage.getItem("history_datasets");
    return d ? JSON.parse(d) : [];
  });
  const [analysis, setAnalysis] = useState(() => {
    const a = localStorage.getItem("history_analysis");
    return a ? JSON.parse(a) : null;
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    fetchHistory();
    // eslint-disable-next-line
  }, []);

  // Sync to localStorage
  useEffect(() => {
    if (datasets && datasets.length > 0)
      localStorage.setItem("history_datasets", JSON.stringify(datasets));
    else localStorage.removeItem("history_datasets");
  }, [datasets]);
  useEffect(() => {
    if (analysis)
      localStorage.setItem("history_analysis", JSON.stringify(analysis));
    else localStorage.removeItem("history_analysis");
  }, [analysis]);

  /* ---------------- API CALLS ---------------- */

  const fetchHistory = async () => {
    try {
      const res = await api.get("history/");
      setDatasets(res.data);
    } catch {
      setError("Failed to load history");
    }
  };

  const analyzeDataset = async (id) => {
    setSelectedId(id);
    setLoading(true);
    setError("");
    setAnalysis(null);

    try {
      const res = await api.get(`dataset/${id}/analyze/`);
      setAnalysis(res.data);
      // ⬇️ smooth auto-scroll
      setTimeout(() => {
        analysisRef.current?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }, 100);
    } catch {
      setError("Failed to analyze dataset");
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = async (id) => {
    try {
      const res = await api.get(`report/${id}/`, {
        responseType: "blob",
      });

      const blob = new Blob([res.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = `dataset_${id}.pdf`;
      document.body.appendChild(a);
      a.click();

      a.remove();
      window.URL.revokeObjectURL(url);
    } catch {
      alert("PDF download failed");
    }
  };

  /* ---------------- RENDER ---------------- */

  return (
    <div className="min-h-screen bg-slate-50 px-6 py-8">
      <div className="max-w-7xl mx-auto">
        {/* HEADER */}
        <div className="mb-6">
          <h2 className="text-3xl font-bold text-slate-900">Upload History</h2>
          <p className="text-slate-600 mt-1">
            View, analyze, and download previously uploaded datasets
          </p>
        </div>

        {error && (
          <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {/* HISTORY TABLE */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-slate-100 text-slate-700">
              <tr>
                <th className="px-4 py-3 text-left">ID</th>
                <th className="px-4 py-3 text-left">Filename</th>
                <th className="px-4 py-3 text-left">Uploaded At</th>
                <th className="px-4 py-3 text-center">Analyze</th>
                <th className="px-4 py-3 text-center">PDF</th>
              </tr>
            </thead>

            <tbody>
              {datasets.map((d) => (
                <tr
                  key={d.id}
                  className={`border-t border-slate-200 transition ${
                    selectedId === d.id
                      ? "bg-blue-50 hover:bg-blue-100"
                      : "hover:bg-slate-50"
                  }`}
                >
                  <td className="px-4 py-3">{d.id}</td>
                  <td className="px-4 py-3 font-medium text-slate-900">
                    {d.name !== null ? d.name : d.filename}
                  </td>
                  <td className="px-4 py-3 text-slate-600">
                    {new Date(d.uploaded_at).toLocaleString()}
                  </td>

                  <td className="px-4 py-3 text-center">
                    <button
                      disabled={loading}
                      onClick={() => analyzeDataset(d.id)}
                      className="px-3 py-1.5 text-sm rounded-md bg-slate-900 text-white hover:bg-slate-800 disabled:bg-slate-400 transition"
                    >
                      Analyze
                    </button>
                  </td>

                  <td className="px-4 py-3 text-center">
                    <button
                      onClick={() => downloadPDF(d.id)}
                      className="px-3 py-1.5 text-sm rounded-md border border-slate-300 hover:bg-slate-100 transition"
                    >
                      Download
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* ANALYSIS SECTION */}
        {loading && <p className="mt-6 text-slate-600">Analyzing dataset…</p>}

        {analysis && !loading && (
          <div ref={analysisRef} className="mt-10 space-y-8">
            <h3 className="text-2xl font-semibold text-slate-900">
              Dataset Analysis
            </h3>

            {/* SUMMARY */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <h4 className="text-lg font-semibold mb-4 text-slate-900">
                Summary
              </h4>

              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                <Stat
                  label="Total Equipment"
                  value={analysis.summary.total_equipment.toString()}
                />
                <Stat
                  label="Avg Flowrate"
                  value={analysis.summary.average_flowrate.toFixed(3)}
                />
                <Stat
                  label="Avg Pressure"
                  value={analysis.summary.average_pressure.toFixed(3)}
                />
                <Stat
                  label="Avg Temperature"
                  value={analysis.summary.average_temperature.toFixed(3)}
                />
              </div>
            </div>

            {/* CHARTS */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <h4 className="text-lg font-semibold mb-4 text-slate-900">
                Charts
              </h4>
              <Charts charts={analysis.charts} />
            </div>

            {/* CSV PREVIEW */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <h4 className="text-lg font-semibold mb-4 text-slate-900">
                CSV Preview
              </h4>
              <CSVPreview rows={analysis.preview} />
            </div>
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
