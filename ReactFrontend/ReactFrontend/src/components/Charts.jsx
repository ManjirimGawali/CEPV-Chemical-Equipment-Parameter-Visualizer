import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
);

export default function Charts({ charts }) {
  /* ---------------- GUARDS ---------------- */
  if (!charts || Object.keys(charts).length === 0) {
    return <EmptyState message="No chart data available yet." />;
  }

  const metricKeys = Object.keys(charts);

  const firstValidKey = metricKeys.find(
    (key) => Array.isArray(charts[key]) && charts[key].length > 0,
  );

  if (!firstValidKey) {
    return <EmptyState message="No numeric values found to visualize." />;
  }

  /* ---------------- DATA ---------------- */
  const labels = charts[firstValidKey].map((_, i) => i + 1);

  const datasets = metricKeys
    .filter((key) => Array.isArray(charts[key]))
    .map((key, index) => ({
      label: formatLabel(key),
      data: charts[key],
      borderColor: COLORS[index % COLORS.length],
      backgroundColor: COLORS[index % COLORS.length],
      tension: 0.35,
      pointRadius: 2,
      pointHoverRadius: 4,
    }));

  const data = { labels, datasets };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top",
        labels: {
          boxWidth: 12,
          boxHeight: 12,
          font: { size: 12 },
        },
      },
      tooltip: {
        mode: "index",
        intersect: false,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Record Index",
          font: { weight: "bold" },
        },
      },
      y: {
        title: {
          display: true,
          text: "Measured Value",
          font: { weight: "bold" },
        },
        beginAtZero: false,
      },
    },
  };

  /* ---------------- UI ---------------- */
  return (
    <div className="bg-white rounded-2xl shadow p-6 space-y-4">
      {/* Header */}
      <div>
        <h3 className="text-lg font-semibold text-slate-900">
          Analytics Overview
        </h3>
        <p className="text-sm text-slate-600">
          Trends across uploaded dataset metrics
        </p>
      </div>

      {/* Chart */}
      <div className="h-[380px]">
        <Line data={data} options={options} />
      </div>

      {/* Footer */}
      <p className="text-xs text-slate-500 text-right">
        Hover over points to inspect values
      </p>
    </div>
  );
}

/* ---------------- HELPERS ---------------- */

function EmptyState({ message }) {
  return (
    <div className="bg-slate-50 border border-dashed border-slate-300 rounded-xl p-8 text-center">
      <p className="text-slate-600 font-medium">{message}</p>
    </div>
  );
}

function formatLabel(key) {
  return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

/* Color palette */
const COLORS = [
  "rgb(54, 162, 235)",
  "rgb(255, 99, 132)",
  "rgb(75, 192, 192)",
  "rgb(153, 102, 255)",
  "rgb(255, 159, 64)",
];
