export default function CSVPreview({ rows }) {
  if (!rows || rows.length === 0) return null;

  const headers = Object.keys(rows[0]);

  return (
    <div className="bg-white rounded-2xl shadow p-6 space-y-4">
      {/* Header */}
      <div>
        <h3 className="text-lg font-semibold text-slate-900">CSV Preview</h3>
        <p className="text-sm text-slate-600">
          Showing first {rows.length} rows from uploaded dataset
        </p>
      </div>

      {/* Table Wrapper */}
      <div className="overflow-x-auto border border-slate-200 rounded-lg">
        <table className="min-w-full text-sm text-left">
          <thead className="bg-slate-100 border-b border-slate-200">
            <tr>
              {headers.map((header) => (
                <th
                  key={header}
                  className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap"
                >
                  {formatHeader(header)}
                </th>
              ))}
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-200">
            {rows.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                className="hover:bg-slate-50 transition-colors"
              >
                {headers.map((header) => (
                  <td
                    key={header}
                    className="px-4 py-2 text-slate-700 whitespace-nowrap"
                  >
                    {row[header]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Footer hint */}
      <p className="text-xs text-slate-500 text-right">
        Scroll horizontally to view all columns
      </p>
    </div>
  );
}

/* -------- helpers -------- */
function formatHeader(header) {
  return header.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}
