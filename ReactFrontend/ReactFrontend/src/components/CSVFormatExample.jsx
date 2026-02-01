export default function CSVFormatExample() {
  const headers = [
    "Equipment Name",
    "Type",
    "Flowrate",
    "Pressure",
    "Temperature",
  ];

  const rows = [
    ["Pump-1", "Pump", 120, 5.2, 110],
    ["Compressor-1", "Compressor", 95, 8.4, 95],
    ["Valve-1", "Valve", 60, 4.1, 105],
    ["HeatExchanger-1", "HeatExchanger", 150, 6.2, 130],
    ["Pump-2", "Pump", 132, 5.6, 118],
    ["Reactor-1", "Reactor", 140, 7.5, 140],
  ];

  return (
    <div className="bg-slate-50 border border-slate-200 rounded-xl p-5">
      <div className="mb-3">
        <h3 className="text-lg font-semibold text-red-500">
          Expected CSV Format *
        </h3>
        <p className="text-xs text-slate-600">
          Your CSV file should follow this structure and column naming
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="bg-slate-100">
              {headers.map((h) => (
                <th
                  key={h}
                  className="px-4 py-2 text-left font-semibold text-slate-700 border-b"
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {rows.map((row, i) => (
              <tr
                key={i}
                className="odd:bg-white even:bg-slate-50 hover:bg-slate-100 transition"
              >
                {row.map((cell, j) => (
                  <td key={j} className="px-4 py-2 text-slate-700 border-b">
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="mt-3 text-xs text-slate-500">
        • Column names are case-insensitive • Numeric fields must contain valid
        numbers • Extra columns will be ignored
      </p>
    </div>
  );
}
