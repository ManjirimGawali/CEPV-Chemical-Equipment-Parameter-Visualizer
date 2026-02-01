export default function TextInput({
  label,
  value,
  onChange,
  placeholder = "",
  type = "text",
  name,
  required = false,
  disabled = false,
  error = "",
  helperText = "",
}) {
  return (
    <div className="space-y-1.5 w-full">
      {/* Label */}
      {label && (
        <label
          htmlFor={name}
          className="block text-sm font-semibold text-slate-900"
        >
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}

      {/* Input */}
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        disabled={disabled}
        required={required}
        className={`
          w-full px-4 py-2.5 rounded-lg border text-sm
          transition-all outline-none
          ${
            error
              ? "border-red-500 focus:ring-2 focus:ring-red-500"
              : "border-slate-300 focus:border-slate-900 focus:ring-2 focus:ring-slate-900"
          }
          ${disabled ? "bg-slate-100 cursor-not-allowed" : "bg-white"}
        `}
      />

      {/* Helper / Error */}
      {error ? (
        <p className="text-xs text-red-600 font-medium">{error}</p>
      ) : (
        helperText && <p className="text-xs text-slate-500">{helperText}</p>
      )}
    </div>
  );
}
