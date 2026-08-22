"use client";

import { useState } from "react";

interface FormState {
  employeeId: string;
  fullName: string;
  email: string;
  password: string;
  confirmPassword: string;
  rememberMe: boolean;
}

interface FormErrors {
  employeeId?: string;
  fullName?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
  general?: string;
}

const initialFormState: FormState = {
  employeeId: "",
  fullName: "",
  email: "",
  password: "",
  confirmPassword: "",
  rememberMe: false,
};

export default function Home() {
  const [isSignUp, setIsSignUp] = useState(false);

  // Backend uses Employee / HR
  const [role, setRole] = useState<"Employee" | "HR">("Employee");

  const [showPassword, setShowPassword] = useState(false);
  const [form, setForm] = useState<FormState>(initialFormState);
  const [errors, setErrors] = useState<FormErrors>({});
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (
    field: keyof FormState,
    value: string | boolean
  ) => {
    setForm((prev) => ({ ...prev, [field]: value }));

    setErrors((prev) => ({
      ...prev,
      [field]: undefined,
      general: undefined,
    }));

    setSubmitted(false);
  };

  const validate = (): FormErrors => {
    const newErrors: FormErrors = {};
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (isSignUp && !form.employeeId.trim()) {
      newErrors.employeeId = "Enter your Employee ID";
    }

    if (isSignUp && !form.fullName.trim()) {
      newErrors.fullName = "Enter your full name";
    }

    if (!form.email.trim()) {
      newErrors.email = "Enter your email address";
    } else if (!emailPattern.test(form.email.trim())) {
      newErrors.email = "Enter a valid email address";
    }

    if (!form.password) {
      newErrors.password = "Enter your password";
    } else if (isSignUp && form.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters";
    }

    if (isSignUp) {
      if (!form.confirmPassword) {
        newErrors.confirmPassword = "Confirm your password";
      } else if (form.confirmPassword !== form.password) {
        newErrors.confirmPassword = "Passwords do not match";
      }
    }

    return newErrors;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const newErrors = validate();
    setErrors(newErrors);

    if (Object.keys(newErrors).length > 0) {
      return;
    }

    setLoading(true);
    setSubmitted(false);

    try {
      const endpoint = isSignUp
        ? "http://127.0.0.1:5000/api/auth/signup"
        : "http://127.0.0.1:5000/api/auth/login";

      const requestBody = isSignUp
        ? {
            employee_id: form.employeeId.trim(),
            email: form.email.trim(),
            password: form.password,
            role: role,
          }
        : {
            email: form.email.trim(),
            password: form.password,
          };

      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();

      if (!response.ok) {
        setErrors({
          general: data.message || "Something went wrong",
        });
        return;
      }

      setSubmitted(true);

      if (isSignUp) {
        // Account successfully created
        setForm(initialFormState);
      } else {
        // Save logged-in user information for the next dashboard step
        localStorage.setItem("employee_id", data.user.employee_id);
        localStorage.setItem("email", data.user.email);
        localStorage.setItem("role", data.user.role);
      }
    } catch (error) {
      console.error(error);

      setErrors({
        general:
          "Cannot connect to the server. Make sure Flask is running on port 5000.",
      });
    } finally {
      setLoading(false);
    }
  };

  const switchMode = () => {
    setIsSignUp(!isSignUp);
    setForm(initialFormState);
    setErrors({});
    setSubmitted(false);
  };

  return (
    <main className="min-h-screen bg-[#070b14] text-white flex items-center justify-center p-6 relative overflow-hidden">

      {/* Background Glow */}
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl" />
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-violet-600/20 rounded-full blur-3xl" />

      {/* Main Card */}
      <div className="relative w-full max-w-5xl grid md:grid-cols-2 bg-white/[0.05] border border-white/10 rounded-3xl overflow-hidden shadow-2xl backdrop-blur-xl">

        {/* LEFT SIDE */}
        <div className="hidden md:flex flex-col justify-between p-12 bg-gradient-to-br from-cyan-500/10 to-violet-600/10">

          <div>
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-cyan-400 to-violet-500 flex items-center justify-center font-bold text-xl">
                D
              </div>

              <div>
                <h1 className="text-xl font-bold">Dayflow</h1>
                <p className="text-xs text-gray-400">
                  Work. Flow. Better.
                </p>
              </div>
            </div>

            {/* Hero Text */}
            <div className="mt-28">
              <p className="text-cyan-300 text-sm font-semibold tracking-wide">
                WORKPLACE MANAGEMENT
              </p>

              <h2 className="text-5xl font-bold leading-tight mt-3">
                Your workday,
                <br />
                <span className="bg-gradient-to-r from-cyan-300 to-violet-400 bg-clip-text text-transparent">
                  simplified.
                </span>
              </h2>

              <p className="mt-6 text-gray-400 leading-7 max-w-md">
                A secure gateway to your workplace. Sign in as an Employee
                or Admin and access your personalized Dayflow workspace.
              </p>
            </div>
          </div>

          <p className="text-xs text-gray-500">
            © 2026 Dayflow • Team ODDO
          </p>
        </div>

        {/* RIGHT SIDE */}
        <div className="p-8 md:p-12">

          {/* Mobile Logo */}
          <div className="md:hidden flex items-center gap-3 mb-10">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-violet-500 flex items-center justify-center font-bold">
              D
            </div>

            <span className="font-bold text-xl">
              Dayflow
            </span>
          </div>

          {/* Heading */}
          <div className="mb-8">
            <p className="text-cyan-300 text-sm font-semibold">
              {isSignUp ? "GET STARTED" : "WELCOME BACK"}
            </p>

            <h2 className="text-3xl font-bold mt-2">
              {isSignUp
                ? "Create your account"
                : "Sign in to Dayflow"}
            </h2>

            <p className="text-gray-400 mt-2">
              {isSignUp
                ? "Create your workplace account."
                : "Access your workplace dashboard."}
            </p>
          </div>

          {/* ROLE SELECTION */}
          <div className="mb-6">
            <p className="text-sm text-gray-300 mb-3">
              Continue as
            </p>

            <div className="grid grid-cols-2 gap-3">

              {/* Employee */}
              <button
                type="button"
                onClick={() => setRole("Employee")}
                aria-pressed={role === "Employee"}
                className={`p-4 rounded-2xl border text-left transition-all ${
                  role === "Employee"
                    ? "border-cyan-400 bg-cyan-400/10 shadow-lg shadow-cyan-500/10"
                    : "border-white/10 bg-white/[0.03] hover:bg-white/[0.07]"
                }`}
              >
                <p className="text-cyan-300 text-xs font-bold tracking-wider mb-2">
                  EMPLOYEE
                </p>

                <p className="font-semibold">
                  Employee
                </p>

                <p className="text-xs text-gray-500 mt-1">
                  Access my workspace
                </p>
              </button>

              {/* HR */}
              <button
                type="button"
                onClick={() => setRole("HR")}
                aria-pressed={role === "HR"}
                className={`p-4 rounded-2xl border text-left transition-all ${
                  role === "HR"
                    ? "border-violet-400 bg-violet-400/10 shadow-lg shadow-violet-500/10"
                    : "border-white/10 bg-white/[0.03] hover:bg-white/[0.07]"
                }`}
              >
                <p className="text-violet-300 text-xs font-bold tracking-wider mb-2">
                  HR
                </p>

                <p className="font-semibold">
                  Admin / HR
                </p>

                <p className="text-xs text-gray-500 mt-1">
                  Manage organization
                </p>
              </button>

            </div>
          </div>

          {/* FORM */}
          <form
            className="space-y-4"
            onSubmit={handleSubmit}
            noValidate
          >

            {/* Employee ID - SIGN UP ONLY */}
            {isSignUp && (
              <div>
                <label
                  htmlFor="employeeId"
                  className="text-sm text-gray-300"
                >
                  Employee ID
                </label>

                <input
                  id="employeeId"
                  type="text"
                  value={form.employeeId}
                  onChange={(e) =>
                    handleChange("employeeId", e.target.value)
                  }
                  placeholder="e.g. EMP001"
                  aria-invalid={!!errors.employeeId}
                  className={`mt-2 w-full rounded-xl border bg-white/[0.05] px-4 py-3 outline-none transition ${
                    errors.employeeId
                      ? "border-red-400 focus:border-red-400"
                      : "border-white/10 focus:border-cyan-400"
                  }`}
                />

                {errors.employeeId && (
                  <p className="mt-1 text-xs text-red-400">
                    {errors.employeeId}
                  </p>
                )}
              </div>
            )}

            {/* Name - Sign Up Only */}
            {isSignUp && (
              <div>
                <label
                  htmlFor="fullName"
                  className="text-sm text-gray-300"
                >
                  Full name
                </label>

                <input
                  id="fullName"
                  type="text"
                  value={form.fullName}
                  onChange={(e) =>
                    handleChange("fullName", e.target.value)
                  }
                  placeholder="Enter your full name"
                  aria-invalid={!!errors.fullName}
                  className={`mt-2 w-full rounded-xl border bg-white/[0.05] px-4 py-3 outline-none transition ${
                    errors.fullName
                      ? "border-red-400 focus:border-red-400"
                      : "border-white/10 focus:border-cyan-400"
                  }`}
                />

                {errors.fullName && (
                  <p className="mt-1 text-xs text-red-400">
                    {errors.fullName}
                  </p>
                )}
              </div>
            )}

            {/* Email */}
            <div>
              <label
                htmlFor="email"
                className="text-sm text-gray-300"
              >
                Email address
              </label>

              <input
                id="email"
                type="email"
                value={form.email}
                onChange={(e) =>
                  handleChange("email", e.target.value)
                }
                placeholder="you@company.com"
                aria-invalid={!!errors.email}
                className={`mt-2 w-full rounded-xl border bg-white/[0.05] px-4 py-3 outline-none transition ${
                  errors.email
                    ? "border-red-400 focus:border-red-400"
                    : "border-white/10 focus:border-cyan-400"
                }`}
              />

              {errors.email && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.email}
                </p>
              )}
            </div>

            {/* Password */}
            <div>
              <label
                htmlFor="password"
                className="text-sm text-gray-300"
              >
                Password
              </label>

              <div className="relative mt-2">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  value={form.password}
                  onChange={(e) =>
                    handleChange("password", e.target.value)
                  }
                  placeholder="Enter your password"
                  aria-invalid={!!errors.password}
                  className={`w-full rounded-xl border bg-white/[0.05] px-4 py-3 pr-16 outline-none transition ${
                    errors.password
                      ? "border-red-400 focus:border-red-400"
                      : "border-white/10 focus:border-cyan-400"
                  }`}
                />

                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-gray-400 hover:text-white"
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>

              {errors.password && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.password}
                </p>
              )}
            </div>

            {/* Confirm Password */}
            {isSignUp && (
              <div>
                <label
                  htmlFor="confirmPassword"
                  className="text-sm text-gray-300"
                >
                  Confirm password
                </label>

                <input
                  id="confirmPassword"
                  type="password"
                  value={form.confirmPassword}
                  onChange={(e) =>
                    handleChange(
                      "confirmPassword",
                      e.target.value
                    )
                  }
                  placeholder="Confirm your password"
                  aria-invalid={!!errors.confirmPassword}
                  className={`mt-2 w-full rounded-xl border bg-white/[0.05] px-4 py-3 outline-none transition ${
                    errors.confirmPassword
                      ? "border-red-400 focus:border-red-400"
                      : "border-white/10 focus:border-cyan-400"
                  }`}
                />

                {errors.confirmPassword && (
                  <p className="mt-1 text-xs text-red-400">
                    {errors.confirmPassword}
                  </p>
                )}
              </div>
            )}

            {/* Login Options */}
            {!isSignUp && (
              <div className="flex items-center justify-between text-sm">

                <label
                  htmlFor="rememberMe"
                  className="flex items-center gap-2 text-gray-400"
                >
                  <input
                    id="rememberMe"
                    type="checkbox"
                    checked={form.rememberMe}
                    onChange={(e) =>
                      handleChange(
                        "rememberMe",
                        e.target.checked
                      )
                    }
                    className="accent-cyan-400"
                  />
                  Remember me
                </label>

                <button
                  type="button"
                  className="text-cyan-300 hover:text-cyan-200"
                >
                  Forgot password?
                </button>

              </div>
            )}

            {/* Error */}
            {errors.general && (
              <p className="text-sm text-red-400 text-center">
                {errors.general}
              </p>
            )}

            {/* Success */}
            {submitted && (
              <p className="text-sm text-cyan-300 text-center">
                {isSignUp
                  ? "Account created successfully!"
                  : "Login successful!"}
              </p>
            )}

            {/* Main Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 rounded-xl font-semibold bg-gradient-to-r from-cyan-400 to-violet-500 text-white hover:scale-[1.02] transition-transform shadow-lg shadow-cyan-500/10 disabled:opacity-60 disabled:hover:scale-100"
            >
              {loading
                ? "Please wait..."
                : isSignUp
                ? `Create ${
                    role === "HR"
                      ? "Admin / HR"
                      : "Employee"
                  } Account`
                : `Continue as ${
                    role === "HR"
                      ? "Admin / HR"
                      : "Employee"
                  }`}
            </button>

          </form>

          {/* Login / Sign Up Switch */}
          <div className="text-center mt-7 text-sm text-gray-400">

            {isSignUp
              ? "Already have an account?"
              : "Don't have an account?"}

            <button
              type="button"
              onClick={switchMode}
              className="ml-2 text-cyan-300 font-semibold hover:text-cyan-200"
            >
              {isSignUp ? "Sign in" : "Create one"}
            </button>

          </div>

        </div>
      </div>
    </main>
  );
}