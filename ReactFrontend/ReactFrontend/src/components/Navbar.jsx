import { NavLink, useNavigate } from "react-router-dom";
import { useState } from "react";
import icon from "../assets/icon.svg";

export default function Navbar() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const linkClass = ({ isActive }) =>
    isActive
      ? "text-green-500 bg-slate-100 rounded-sm p-1 font-semibold m-2"
      : "text-slate-600 hover:text-slate-900 m-2 font-semibold transition-colors";

  return (
    <header className="bg-white border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-2">
          <img src={icon} alt="icon" className="w-16 h-16" />
          <span className="text-2xl font-bold text-slate-900">CEPV</span>
          <span className="hidden sm:block text-md text-slate-500">
            Chemical Equipment Parameter Visualizer
          </span>
        </div>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-6">
          <NavLink to="/dashboard" className={linkClass}>
            Dashboard
          </NavLink>

          <NavLink to="/history" className={linkClass}>
            History
          </NavLink>

          <span className="h-6 w-px bg-slate-300" />

          <button
            onClick={logout}
            className="px-4 py-2 rounded-lg bg-slate-900 text-white text-sm font-semibold hover:bg-slate-800 transition-colors"
          >
            Logout
          </button>
        </nav>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setOpen(!open)}
          className="md:hidden p-2 rounded-lg border border-slate-300 text-slate-700"
        >
          ☰
        </button>
      </div>

      {/* Mobile Menu */}
      {open && (
        <div className="md:hidden border-t border-slate-200 bg-white px-6 py-6 space-y-6">
          <NavLink
            to="/dashboard"
            onClick={() => setOpen(false)}
            className={linkClass}
          >
            Dashboard
          </NavLink>

          <NavLink
            to="/history"
            onClick={() => setOpen(false)}
            className={linkClass}
          >
            History
          </NavLink>

          <button
            onClick={logout}
            className="w-full mt-4 text-left px-4 py-2 rounded-lg bg-slate-900 text-white text-sm font-semibold hover:bg-slate-800 transition-colors"
          >
            Logout
          </button>
        </div>
      )}
    </header>
  );
}
