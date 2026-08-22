"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  const [employeeId, setEmployeeId] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("");

  useEffect(() => {
    const storedEmployeeId = localStorage.getItem("employee_id");
    const storedEmail = localStorage.getItem("email");
    const storedRole = localStorage.getItem("role");

    if (!storedEmployeeId || !storedEmail || !storedRole) {
      router.push("/");
      return;
    }

    setEmployeeId(storedEmployeeId);
    setEmail(storedEmail);
    setRole(storedRole);
  }, [router]);

  const logout = () => {
    localStorage.removeItem("employee_id");
    localStorage.removeItem("email");
    localStorage.removeItem("role");

    router.push("/");
  };

  return (
    <main className="min-h-screen bg-[#070b14] text-white">

      {/* Header */}
      <header className="border-b border-white/10 bg-white/[0.03]">
        <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">

          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-cyan-400 to-violet-500 flex items-center justify-center font-bold text-xl">
              D
            </div>

            <div>
              <h1 className="font-bold text-xl">
                Dayflow
              </h1>

              <p className="text-xs text-gray-500">
                Work. Flow. Better.
              </p>
            </div>
          </div>

          <button
            onClick={logout}
            className="px-4 py-2 rounded-xl border border-white/10 hover:bg-white/10 transition"
          >
            Logout
          </button>

        </div>
      </header>

      {/* Dashboard */}
      <div className="max-w-7xl mx-auto px-6 py-10">

        <div className="mb-10">
          <p className="text-cyan-300 text-sm font-semibold">
            DASHBOARD
          </p>

          <h2 className="text-4xl font-bold mt-2">
            Welcome to Dayflow 👋
          </h2>

          <p className="text-gray-400 mt-2">
            Manage your workday from one place.
          </p>
        </div>

        {/* User Card */}
        <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-7 mb-8">

          <div className="flex items-center justify-between">

            <div>
              <p className="text-gray-500 text-sm">
                Employee ID
              </p>

              <p className="text-2xl font-bold mt-1">
                {employeeId}
              </p>
            </div>

            <div>
              <p className="text-gray-500 text-sm">
                Email
              </p>

              <p className="font-medium mt-1">
                {email}
              </p>
            </div>

            <div>
              <p className="text-gray-500 text-sm">
                Role
              </p>

              <p className="text-cyan-300 font-semibold mt-1">
                {role}
              </p>
            </div>

          </div>

        </div>

        {/* Dashboard Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">

          <DashboardCard
            title="Attendance"
            description="View your attendance and check-in details."
          />

          <DashboardCard
            title="Leave Requests"
            description="Apply for leave and track your requests."
          />

          <DashboardCard
            title="Profile"
            description="View and manage your employee profile."
          />

        </div>

      </div>

    </main>
  );
}

function DashboardCard({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-6 hover:bg-white/[0.07] transition">

      <div className="w-10 h-10 rounded-xl bg-cyan-400/10 flex items-center justify-center text-cyan-300 mb-5">
        ●
      </div>

      <h3 className="text-xl font-semibold">
        {title}
      </h3>

      <p className="text-gray-400 text-sm mt-2 leading-6">
        {description}
      </p>

    </div>
  );
}