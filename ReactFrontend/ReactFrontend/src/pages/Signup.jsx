import React, { useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";
import { useNavigate } from "react-router-dom";

export default function SignupPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const validateForm = () => {
    if (!username.trim()) {
      setError("Username is required");
      return false;
    }
    if (username.length < 3) {
      setError("Username must be at least 3 characters");
      return false;
    }
    if (!password) {
      setError("Password is required");
      return false;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return false;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return false;
    }
    return true;
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      await api.post("auth/signup/", {
        username,
        password,
      });

      setSuccess(true);
      setUsername("");
      setPassword("");
      setConfirmPassword("");
    } catch (err) {
      setError("An error occurred. Please try again.");
      console.error("Signup error:", err);
    } finally {
      setLoading(false);
      navigate("/login");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-slate-900 mb-2">
            Create Account
          </h1>
          <p className="text-slate-600">Join us today to get started</p>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 space-y-6">
          {/* Error Alert */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-700 text-sm font-medium">{error}</p>
            </div>
          )}

          {/* Success Alert */}
          {success && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <p className="text-green-700 text-sm font-medium">
                Account created successfully! Redirecting to login...
              </p>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSignup} className="space-y-5">
            {/* Username Field */}
            <div className="space-y-2">
              <label
                htmlFor="username"
                className="block text-sm font-semibold text-slate-900"
              >
                Username
              </label>
              <input
                id="username"
                type="text"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={loading}
                autoComplete="username"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-transparent disabled:bg-slate-50 disabled:cursor-not-allowed transition-all"
              />
            </div>

            {/* Password Field */}
            <div className="space-y-2">
              <label
                htmlFor="password"
                className="block text-sm font-semibold text-slate-900"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                placeholder="Create a password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
                autoComplete="new-password"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-transparent disabled:bg-slate-50 disabled:cursor-not-allowed transition-all"
              />
              <p className="text-xs text-slate-500">
                Must be at least 6 characters
              </p>
            </div>

            {/* Confirm Password Field */}
            <div className="space-y-2">
              <label
                htmlFor="confirmPassword"
                className="block text-sm font-semibold text-slate-900"
              >
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                type="password"
                placeholder="Confirm your password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                disabled={loading}
                autoComplete="new-password"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-transparent disabled:bg-slate-50 disabled:cursor-not-allowed transition-all"
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 bg-slate-900 text-white font-semibold rounded-lg hover:bg-slate-800 disabled:bg-slate-500 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center gap-2 mt-6"
            >
              {loading ? (
                <>
                  <span className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent" />
                  Creating account...
                </>
              ) : (
                "Create account"
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="relative pt-2">
            <div className="border-t border-slate-300"></div>
          </div>

          {/* Login Link */}
          <div className="text-center">
            <p className="text-slate-600 text-sm">
              Already have an account?{" "}
              <Link
                to="/login"
                className="font-semibold text-slate-900 hover:text-slate-700 transition-colors"
              >
                Sign in
              </Link>
            </p>
          </div>
        </div>

        {/* Footer Links */}
        <div className="text-center text-xs text-slate-500 mt-8 space-y-2">
          <p>
            By creating an account, you agree to our{" "}
            <a
              href="#"
              className="text-slate-700 hover:text-slate-900 underline transition-colors"
            >
              Terms of Service
            </a>{" "}
            and{" "}
            <a
              href="#"
              className="text-slate-700 hover:text-slate-900 underline transition-colors"
            >
              Privacy Policy
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
