import { useEffect, useMemo, useState } from "react";

const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
  
const INCIDENTS = [
  {
    id: "fire",
    label: "Fire",
    sub: "Fire & smoke",
    icon: "🔥",
  },
  {
    id: "chemical_leak",
    label: "Hazmat",
    sub: "Chemical release",
    icon: "⚠",
  },
  {
    id: "intrusion",
    label: "Intrusion",
    sub: "Unauthorized access",
    icon: "◉",
  },
  {
    id: "accident",
    label: "Medical",
    sub: "Accident response",
    icon: "✚",
  },
  {
    id: "structural_damage",
    label: "Structural",
    sub: "Damage inspection",
    icon: "◇",
  },
  {
    id: "flooding",
    label: "Flood",
    sub: "Area mapping",
    icon: "≈",
  },
];

/* =========================================================
   ICON
========================================================= */

function Icon({ name, size = 18 }) {
  const paths = {
    drone: (
      <>
        <path d="M8 9h8l2 3-2 3H8l-2-3 2-3Z" />
        <path d="M6 12H2.5M21.5 12H18" />
        <path d="M9 9 6.5 6M15 9l2.5-3" />
        <path d="M9 15 6.5 18M15 15l2.5 3" />
        <circle cx="6.5" cy="6" r="1.4" />
        <circle cx="17.5" cy="6" r="1.4" />
        <circle cx="6.5" cy="18" r="1.4" />
        <circle cx="17.5" cy="18" r="1.4" />
      </>
    ),

    grid: (
      <>
        <rect x="3" y="3" width="7" height="7" rx="1" />
        <rect x="14" y="3" width="7" height="7" rx="1" />
        <rect x="3" y="14" width="7" height="7" rx="1" />
        <rect x="14" y="14" width="7" height="7" rx="1" />
      </>
    ),

    brain: (
      <>
        <path d="M9.5 4.5A3 3 0 0 0 6 7.3 3 3 0 0 0 4.5 12 3 3 0 0 0 7 16.8 3 3 0 0 0 12 19V7a3 3 0 0 0-2.5-2.5Z" />
        <path d="M14.5 4.5A3 3 0 0 1 18 7.3a3 3 0 0 1 1.5 4.7 3 3 0 0 1-2.5 4.8A3 3 0 0 1 12 19V7a3 3 0 0 1 2.5-2.5Z" />
        <path d="M8 9h1m-2 4h2m7-4h-1m2 4h-2" />
      </>
    ),

    shield: (
      <>
        <path d="M12 3 20 6v5c0 5-3.4 8.3-8 10-4.6-1.7-8-5-8-10V6l8-3Z" />
        <path d="m9 12 2 2 4-4" />
      </>
    ),

    alert: (
      <>
        <path d="m12 3 9 17H3L12 3Z" />
        <path d="M12 9v4m0 3h.01" />
      </>
    ),

    refresh: (
      <>
        <path d="M20 11a8 8 0 0 0-14.8-4L3 10" />
        <path d="M3 5v5h5" />
        <path d="M4 13a8 8 0 0 0 14.8 4L21 14" />
        <path d="M21 19v-5h-5" />
      </>
    ),

    logout: (
      <>
        <path d="M10 17l5-5-5-5" />
        <path d="M15 12H3" />
        <path d="M21 3v18" />
      </>
    ),

    eye: (
      <>
        <path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z" />
        <circle cx="12" cy="12" r="2.5" />
      </>
    ),
  };

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      {paths[name]}
    </svg>
  );
}

/* =========================================================
   STATUS
========================================================= */

function StatusDot({
  type = "success",
  pulse = false,
}) {
  const color =
    type === "warning"
      ? "bg-amber-400"
      : type === "danger"
        ? "bg-red-400"
        : type === "blue"
          ? "bg-cyan-400"
          : "bg-emerald-400";

  return (
    <span
      className={`relative inline-block h-2 w-2 rounded-full ${color}`}
    >
      {pulse && (
        <span
          className={`absolute inset-0 animate-ping rounded-full ${color} opacity-60`}
        />
      )}
    </span>
  );
}

/* =========================================================
   BRAND
========================================================= */

function Brand() {
  return (
    <div className="flex items-center gap-3">

      <div className="relative flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-400/30 bg-cyan-400/[0.07] text-cyan-300 shadow-[0_0_30px_rgba(34,211,238,.08)]">

        <Icon
          name="drone"
          size={20}
        />

      </div>

      <div>

        <p className="text-sm font-bold tracking-[0.14em] text-white">
          DRONERESCUE
        </p>

        <p className="mt-1 text-[10px] uppercase tracking-[0.22em] text-slate-600">
          Autonomous response
        </p>

      </div>

    </div>
  );
}

/* =========================================================
   LOGIN
========================================================= */

function Login({
  email,
  password,
  setEmail,
  setPassword,
  error,
  showPassword,
  setShowPassword,
  onSubmit,
}) {
  return (
    <div className="relative min-h-screen overflow-hidden bg-[#03060b] text-white">

      {/* cinematic atmosphere */}

      <div className="pointer-events-none absolute inset-0">

        <div className="absolute left-[-15%] top-[-20%] h-[650px] w-[650px] rounded-full bg-cyan-500/[0.08] blur-[150px]" />

        <div className="absolute right-[-15%] bottom-[-20%] h-[700px] w-[700px] rounded-full bg-blue-600/[0.08] blur-[160px]" />

        <div
          className="absolute inset-0 opacity-[0.06]"
          style={{
            backgroundImage:
              "linear-gradient(rgba(148,163,184,.3) 1px, transparent 1px),linear-gradient(90deg,rgba(148,163,184,.3) 1px,transparent 1px)",
            backgroundSize: "70px 70px",
          }}
        />

      </div>

      <div className="relative flex min-h-screen items-center justify-center px-6 py-10">

        <div className="grid w-full max-w-6xl overflow-hidden rounded-[30px] border border-white/[0.09] bg-[#080c13]/95 shadow-[0_40px_120px_rgba(0,0,0,.7)] lg:grid-cols-[1.1fr_.9fr]">

          {/* LEFT */}

          <div className="relative hidden min-h-[700px] overflow-hidden border-r border-white/[0.07] lg:block">

            <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_45%,rgba(34,211,238,.08),transparent_40%)]" />

            <div
              className="absolute inset-0 opacity-[0.08]"
              style={{
                backgroundImage:
                  "linear-gradient(rgba(34,211,238,.5) 1px,transparent 1px),linear-gradient(90deg,rgba(34,211,238,.5) 1px,transparent 1px)",
                backgroundSize: "80px 80px",
              }}
            />

            {/* radar */}

            <div className="absolute left-1/2 top-[46%] h-[360px] w-[360px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-cyan-400/10">

              <div className="absolute inset-8 rounded-full border border-cyan-400/[0.08]" />

              <div className="absolute inset-20 rounded-full border border-cyan-400/[0.07]" />

              <div className="absolute left-1/2 top-1/2 h-px w-1/2 origin-left rotate-[-30deg] bg-gradient-to-r from-cyan-400/60 to-transparent" />

              <div className="absolute left-1/2 top-1/2 h-3 w-3 -translate-x-1/2 -translate-y-1/2 rounded-full bg-cyan-300 shadow-[0_0_30px_8px_rgba(34,211,238,.2)]" />

            </div>

            <div className="relative p-12">

              <Brand />

              <div className="mt-40 max-w-xl">

                <p className="text-xs font-semibold uppercase tracking-[0.35em] text-cyan-400">
                  Autonomous aerial intelligence
                </p>

                <h1 className="mt-6 text-6xl font-semibold leading-[.98] tracking-[-0.05em]">

                  From signal

                  <span className="block text-slate-600">
                    to response.
                  </span>

                </h1>

                <p className="mt-7 max-w-md text-base leading-8 text-slate-500">
                  Intelligent emergency response infrastructure
                  connecting autonomous drones, computer vision,
                  operational knowledge and human oversight.
                </p>

              </div>

              <div className="absolute bottom-12 left-12 right-12 grid grid-cols-3 gap-3">

                <LoginMetric
                  value="24/7"
                  label="Mission coverage"
                />

                <LoginMetric
                  value="AI"
                  label="Decision engine"
                />

                <LoginMetric
                  value="HITL"
                  label="Safety control"
                />

              </div>

            </div>

          </div>

          {/* RIGHT */}

          <div className="flex min-h-[700px] items-center p-8 sm:p-14">

            <div className="mx-auto w-full max-w-md">

              <div className="lg:hidden">
                <Brand />
              </div>

              <div className="mt-12 lg:mt-0">

                <div className="inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/[0.04] px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.12em] text-emerald-300">

                  <StatusDot pulse />

                  Secure operations portal

                </div>

                <h2 className="mt-7 text-4xl font-semibold tracking-[-0.035em]">
                  Welcome back
                </h2>

                <p className="mt-3 text-base text-slate-500">
                  Sign in to Mission Control.
                </p>

              </div>

              <form
                onSubmit={onSubmit}
                className="mt-10 space-y-6"
              >

                <div>

                  <label className="mb-2.5 block text-sm font-medium text-slate-400">
                    Operator email
                  </label>

                  <input
                    value={email}
                    onChange={(e) =>
                      setEmail(e.target.value)
                    }
                    type="email"
                    className="w-full rounded-xl border border-white/[0.09] bg-white/[0.025] px-4 py-4 text-sm outline-none transition focus:border-cyan-400/50 focus:bg-white/[0.045]"
                  />

                </div>

                <div>

                  <label className="mb-2.5 block text-sm font-medium text-slate-400">
                    Password
                  </label>

                  <div className="relative">

                    <input
                      value={password}
                      onChange={(e) =>
                        setPassword(e.target.value)
                      }
                      type={
                        showPassword
                          ? "text"
                          : "password"
                      }
                      className="w-full rounded-xl border border-white/[0.09] bg-white/[0.025] px-4 py-4 pr-12 text-sm outline-none transition focus:border-cyan-400/50 focus:bg-white/[0.045]"
                    />

                    <button
                      type="button"
                      onClick={() =>
                        setShowPassword(
                          !showPassword
                        )
                      }
                      className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-600 hover:text-slate-300"
                    >
                      <Icon
                        name="eye"
                        size={18}
                      />
                    </button>

                  </div>

                </div>

                {error && (
                  <div className="rounded-xl border border-red-400/20 bg-red-400/[0.05] px-4 py-3 text-sm text-red-300">
                    {error}
                  </div>
                )}

                <button
                  type="submit"
                  className="group w-full rounded-xl bg-cyan-400 px-5 py-4 text-sm font-bold tracking-wide text-[#031017] transition hover:bg-cyan-300 hover:shadow-[0_0_40px_rgba(34,211,238,.15)]"
                >
                  ENTER MISSION CONTROL
                </button>

              </form>

              <div className="mt-10 border-t border-white/[0.06] pt-6">

                <p className="text-xs text-slate-600">
                  Demonstration environment
                </p>

                <p className="mt-2 font-mono text-xs text-slate-700">
                  operator@dronerescue.ai
                </p>

                <p className="mt-1 font-mono text-xs text-slate-700">
                  demo123
                </p>

              </div>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

function LoginMetric({ value, label }) {
  return (
    <div className="rounded-xl border border-white/[0.07] bg-black/20 p-4 backdrop-blur">
      <p className="text-lg font-semibold">
        {value}
      </p>

      <p className="mt-1 text-xs text-slate-600">
        {label}
      </p>
    </div>
  );
}

/* =========================================================
   MAIN APPLICATION
========================================================= */

export default function App() {

  const [authenticated, setAuthenticated] =
    useState(
      localStorage.getItem(
        "dronerescue-auth"
      ) === "true"
    );

  const [email, setEmail] = useState(
    "operator@dronerescue.ai"
  );

  const [password, setPassword] =
    useState("demo123");

  const [showPassword, setShowPassword] =
    useState(false);

  const [loginError, setLoginError] =
    useState("");

  const [drones, setDrones] = useState([]);

  const [missions, setMissions] =
    useState([]);

  const [approvals, setApprovals] =
    useState([]);

  const [incident, setIncident] =
    useState("fire");

  const [triggering, setTriggering] =
    useState(false);

  const [result, setResult] =
    useState(null);

  const [connected, setConnected] =
    useState(false);

  const [activeNav, setActiveNav] =
    useState("Operations");

  const [busyMission, setBusyMission] =
    useState(null);

  /* =======================================================
     LOGIN
  ======================================================= */

  function handleLogin(event) {

    event.preventDefault();

    if (
      email === "operator@dronerescue.ai" &&
      password === "demo123"
    ) {

      localStorage.setItem(
        "dronerescue-auth",
        "true"
      );

      setAuthenticated(true);
      setLoginError("");

    } else {

      setLoginError(
        "Access denied. Check your operator credentials."
      );

    }
  }

  function logout() {

    localStorage.removeItem(
      "dronerescue-auth"
    );

    setAuthenticated(false);
  }

  /* =======================================================
     BACKEND
  ======================================================= */

  async function loadDashboard() {

    try {

      const [
        droneResponse,
        missionResponse,
        approvalResponse,
      ] = await Promise.all([
        fetch(`${API_URL}/drones`),
        fetch(`${API_URL}/drones/missions`),
        fetch(`${API_URL}/drones/approvals`),
      ]);

      if (!droneResponse.ok) {
        throw new Error(
          "Fleet unavailable"
        );
      }

      const droneData =
        await droneResponse.json();

      setDrones(
        droneData.drones || []
      );

      setConnected(true);

      if (missionResponse.ok) {

        const missionData =
          await missionResponse.json();

        setMissions(
          missionData.missions || []
        );

      }

      if (approvalResponse.ok) {

        const approvalData =
          await approvalResponse.json();

        setApprovals(
          approvalData.approvals || []
        );

      }

    } catch (error) {

      console.error(error);

      setConnected(false);

    }
  }

  useEffect(() => {

    if (!authenticated) {
      return;
    }

    loadDashboard();

    const timer = setInterval(
      loadDashboard,
      3000
    );

    return () =>
      clearInterval(timer);

  }, [authenticated]);

  /* =======================================================
     EMERGENCY DISPATCH
  ======================================================= */

  async function triggerEmergency() {

    setTriggering(true);
    setResult(null);

    try {

      const response =
        await fetch(
          `${API_URL}/drones/emergency`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({
              incident_type:
                incident,

              location: {
                latitude: 17.6868,
                longitude: 83.2185,
              },

              source:
                "mission_control",

              confidence: 0.95,

              description:
                `${incident} emergency detected`,
            }),
          }
        );

      const data =
        await response.json();

      if (!response.ok) {

        throw new Error(
          data.detail?.status ||
          data.detail?.reason ||
          "Mission dispatch failed"
        );

      }

      setResult(data);

      await loadDashboard();

    } catch (error) {

      setResult({
        error: error.message,
      });

    } finally {

      setTriggering(false);

    }
  }

  /* =======================================================
     HITL
  ======================================================= */

  async function resolveApproval(
    missionId,
    approved
  ) {

    setBusyMission(missionId);

    try {

      const response =
        await fetch(
          `${API_URL}/drones/approvals/${missionId}/resolve`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({
              approved,

              operator:
                "mission_control_operator",
            }),
          }
        );

      const data =
        await response.json();

      if (!response.ok) {

        throw new Error(
          data.detail?.reason ||
          "Approval failed"
        );

      }

      setResult(data);

      await loadDashboard();

    } catch (error) {

      setResult({
        error: error.message,
      });

    } finally {

      setBusyMission(null);

    }
  }

  /* =======================================================
     DERIVED DATA
  ======================================================= */

  const activeDrones =
    drones.filter(
      (drone) =>
        drone.status !== "offline"
    ).length;

  const aiDecisions =
    missions.reduce(
      (total, mission) =>
        total +
        (mission.decisions?.length || 0),
      0
    );

  const averageBattery =
    drones.length
      ? Math.round(
          drones.reduce(
            (total, drone) =>
              total + drone.battery,
            0
          ) / drones.length
        )
      : 0;

  const latestMission =
    missions[0];

  const latestObservation =
    latestMission?.observations?.[
      latestMission.observations.length - 1
    ];

  const latestAnalysis =
    latestObservation?.analysis;

  const latestDecision =
    latestMission?.decisions?.[
      latestMission.decisions.length - 1
    ];

  const needsApproval =
    latestMission?.status ===
    "human_review_required";

  const missionCompleted =
    latestMission?.status ===
      "mission_completed" ||
    latestMission?.status ===
      "completed";

  /* =======================================================
     LOGIN
  ======================================================= */

  if (!authenticated) {

    return (
      <Login
        email={email}
        password={password}
        setEmail={setEmail}
        setPassword={setPassword}
        error={loginError}
        showPassword={showPassword}
        setShowPassword={
          setShowPassword
        }
        onSubmit={handleLogin}
      />
    );
  }

  /* =======================================================
     DASHBOARD
  ======================================================= */

  return (
    <div className="relative min-h-screen overflow-x-hidden bg-[#03060b] text-slate-100">

      {/* ===================================================
          GLOBAL ATMOSPHERE
      =================================================== */}

      <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden">

        <div className="absolute left-[-15%] top-[-15%] h-[55rem] w-[55rem] rounded-full bg-cyan-500/[0.045] blur-[160px]" />

        <div className="absolute right-[-15%] top-[10%] h-[50rem] w-[50rem] rounded-full bg-blue-600/[0.04] blur-[160px]" />

        <div className="absolute bottom-[-20%] left-[30%] h-[45rem] w-[45rem] rounded-full bg-indigo-500/[0.025] blur-[150px]" />

        <div
          className="absolute inset-0 opacity-[0.035]"
          style={{
            backgroundImage:
              "linear-gradient(rgba(148,163,184,.3) 1px, transparent 1px),linear-gradient(90deg,rgba(148,163,184,.3) 1px,transparent 1px)",
            backgroundSize: "80px 80px",
          }}
        />

        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,transparent_0%,rgba(3,6,11,.2)_50%,rgba(3,6,11,.92)_100%)]" />

      </div>

      <div className="relative z-10 flex min-h-screen">

        {/* =================================================
            SIDEBAR
        ================================================= */}

        <aside className="hidden w-[255px] shrink-0 border-r border-white/[0.06] bg-[#060a10]/90 backdrop-blur-xl lg:flex lg:flex-col">

          <div className="px-7 py-7">
            <Brand />
          </div>

          <div className="px-4">

            <p className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[0.25em] text-slate-700">
              Mission control
            </p>

            {[
              ["Operations", "grid"],
              ["Fleet", "drone"],
              ["Missions", "mission"],
              ["Intelligence", "brain"],
            ].map(
              ([name, icon]) => {

                const active =
                  activeNav === name;

                return (
                  <button
                    key={name}
                    onClick={() =>
                      setActiveNav(name)
                    }
                    className={`mb-1 flex w-full items-center gap-3 rounded-xl px-4 py-3.5 text-sm transition ${
                      active
                        ? "border border-white/[0.05] bg-white/[0.055] text-white shadow-[0_8px_30px_rgba(0,0,0,.2)]"
                        : "text-slate-500 hover:bg-white/[0.025] hover:text-slate-300"
                    }`}
                  >

                    <Icon
                      name={icon}
                      size={18}
                    />

                    {name}

                    {name ===
                      "Operations" &&
                      approvals.length >
                        0 && (
                        <span className="ml-auto rounded-full bg-amber-400/10 px-2 py-0.5 text-[10px] font-semibold text-amber-300">
                          {approvals.length}
                        </span>
                      )}

                  </button>
                );
              }
            )}

          </div>

          <div className="mt-auto border-t border-white/[0.06] p-5">

            <div className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-4">

              <div className="flex items-center gap-2">

                <StatusDot
                  type={
                    connected
                      ? "success"
                      : "danger"
                  }
                  pulse={connected}
                />

                <span className="text-xs font-medium">
                  {connected
                    ? "Systems nominal"
                    : "Connection lost"}
                </span>

              </div>

              <div className="mt-4 grid grid-cols-2 gap-3">

                <SmallSystem
                  label="RAG"
                  value="READY"
                />

                <SmallSystem
                  label="VISION"
                  value="READY"
                />

                <SmallSystem
                  label="SAFETY"
                  value="ACTIVE"
                />

                <SmallSystem
                  label="HITL"
                  value="ENABLED"
                />

              </div>

            </div>

            <button
              onClick={logout}
              className="mt-4 flex items-center gap-2 px-3 py-2 text-xs text-slate-600 transition hover:text-slate-300"
            >

              <Icon
                name="logout"
                size={15}
              />

              Sign out

            </button>

          </div>

        </aside>

        {/* =================================================
            MAIN
        ================================================= */}

        <main className="min-w-0 flex-1">

          {/* HEADER */}

          <header className="sticky top-0 z-40 border-b border-white/[0.06] bg-[#03060b]/80 backdrop-blur-2xl">

            <div className="flex h-[76px] items-center justify-between px-5 sm:px-8 lg:px-10">

              <div>

                <p className="text-sm font-medium text-slate-300">
                  {activeNav}
                </p>

                <p className="mt-1 text-xs text-slate-600">
                  Mission Control / Live environment
                </p>

              </div>

              <div className="flex items-center gap-4">

                <button
                  onClick={
                    loadDashboard
                  }
                  className="rounded-xl border border-white/[0.08] bg-white/[0.02] p-2.5 text-slate-500 transition hover:border-white/[0.15] hover:text-white"
                >
                  <Icon
                    name="refresh"
                    size={17}
                  />
                </button>

                <div className="hidden items-center gap-2.5 rounded-full border border-emerald-400/15 bg-emerald-400/[0.035] px-4 py-2 sm:flex">

                  <StatusDot
                    pulse
                  />

                  <span className="text-[11px] font-semibold uppercase tracking-wider text-emerald-300">
                    System operational
                  </span>

                </div>

                <div className="h-8 w-px bg-white/[0.06]" />

                <div className="flex items-center gap-3">

                  <div className="flex h-10 w-10 items-center justify-center rounded-full border border-cyan-400/20 bg-cyan-400/[0.06] text-xs font-semibold text-cyan-300">
                    MC
                  </div>

                  <div className="hidden sm:block">

                    <p className="text-xs font-medium">
                      Mission Control
                    </p>

                    <p className="mt-1 text-xs text-slate-600">
                      Operator
                    </p>

                  </div>

                </div>

              </div>

            </div>

          </header>

          {/* =================================================
              PAGE
          ================================================= */}

          <div className="mx-auto max-w-[1800px] px-5 py-8 sm:px-8 lg:px-10">

            {/* HERO */}

            <section className="mb-8 flex flex-col justify-between gap-6 xl:flex-row xl:items-end">

              <div>

                <div className="flex items-center gap-2 text-[11px] font-semibold uppercase tracking-[0.3em] text-cyan-400">

                  <StatusDot
                    type="blue"
                    pulse
                  />

                  Live operations

                </div>

                <h1 className="mt-4 bg-gradient-to-r from-white via-slate-100 to-slate-500 bg-clip-text text-4xl font-semibold tracking-[-0.045em] text-transparent sm:text-5xl lg:text-6xl">
                  Emergency response
                </h1>

                <p className="mt-4 text-base text-slate-500">
                  Autonomous aerial operations and
                  mission intelligence.
                </p>

              </div>

              {/* KPI STRIP */}

              <div className="grid grid-cols-3 overflow-hidden rounded-2xl border border-white/[0.08] bg-white/[0.02] shadow-[0_15px_50px_rgba(0,0,0,.2)]">

                <KPI
                  label="Fleet"
                  value={activeDrones}
                />

                <KPI
                  label="Missions"
                  value={missions.length}
                />

                <KPI
                  label="AI decisions"
                  value={aiDecisions}
                />

              </div>

            </section>

            {/* =================================================
                MAP + FLEET
            ================================================= */}

            <section className="mb-6 grid gap-6 xl:grid-cols-[1.7fr_.75fr]">

              {/* MAP */}

              <div className="relative min-h-[520px] overflow-hidden rounded-[22px] border border-white/[0.09] bg-[#070d15]/90 shadow-[0_30px_100px_rgba(0,0,0,.35)] backdrop-blur-xl">

                {/* atmosphere */}

                <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_52%,rgba(34,211,238,.08),transparent_38%)]" />

                {/* map grid */}

                <div
                  className="absolute inset-0 opacity-[0.18]"
                  style={{
                    backgroundImage:
                      "linear-gradient(rgba(71,85,105,.3) 1px,transparent 1px),linear-gradient(90deg,rgba(71,85,105,.3) 1px,transparent 1px)",
                    backgroundSize: "58px 58px",
                  }}
                />

                {/* topographic lines */}

                <div className="absolute left-[5%] top-[30%] h-[220px] w-[40%] rounded-[50%] border border-cyan-400/[0.07] rotate-12" />

                <div className="absolute left-[12%] top-[35%] h-[180px] w-[36%] rounded-[50%] border border-cyan-400/[0.05] rotate-12" />

                <div className="absolute right-[10%] top-[20%] h-[300px] w-[45%] rounded-[50%] border border-white/[0.035] -rotate-12" />

                {/* header */}

                <div className="relative z-10 flex items-center justify-between border-b border-white/[0.06] px-6 py-5">

                  <div>

                    <p className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-300">
                      Live geospatial operations
                    </p>

                    <p className="mt-1.5 font-mono text-xs text-slate-600">
                      17.6868° N · 83.2185° E
                    </p>

                  </div>

                  <div className="flex items-center gap-2 text-[10px] font-semibold uppercase tracking-wider text-cyan-400">

                    <StatusDot
                      type="blue"
                      pulse
                    />

                    Live telemetry

                  </div>

                </div>

                {/* radar */}

                <div className="absolute left-[48%] top-[52%] h-[300px] w-[300px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-red-400/[0.06]">

                  <div className="absolute inset-[25%] rounded-full border border-red-400/[0.08]" />

                  <div className="absolute inset-[12%] rounded-full border border-red-400/[0.05]" />

                  <div className="absolute left-1/2 top-1/2 h-px w-1/2 origin-left animate-[spin_7s_linear_infinite] bg-gradient-to-r from-red-400/50 to-transparent" />

                </div>

                {/* flight paths */}

                <svg
                  className="absolute inset-0 h-full w-full opacity-60"
                  viewBox="0 0 1000 500"
                  preserveAspectRatio="none"
                >

                  <path
                    d="M245 170 C350 215 420 260 500 260"
                    stroke="rgba(34,211,238,.45)"
                    strokeWidth="1.5"
                    strokeDasharray="7 9"
                    fill="none"
                  />

                  <path
                    d="M720 320 C640 300 570 275 500 260"
                    stroke="rgba(34,211,238,.32)"
                    strokeWidth="1.5"
                    strokeDasharray="7 9"
                    fill="none"
                  />

                  <path
                    d="M525 150 C520 195 510 225 500 260"
                    stroke="rgba(34,211,238,.3)"
                    strokeWidth="1.5"
                    strokeDasharray="7 9"
                    fill="none"
                  />

                </svg>

                {/* drone markers */}

                <MapDrone
                  id="D1"
                  name="Rescue-01"
                  left="28%"
                  top="32%"
                />

                <MapDrone
                  id="D3"
                  name="Rescue-03"
                  left="53%"
                  top="28%"
                  active
                />

                <MapDrone
                  id="D2"
                  name="Rescue-02"
                  left="72%"
                  top="62%"
                />

                {/* incident */}

                <div className="absolute left-[50%] top-[52%] -translate-x-1/2 -translate-y-1/2">

                  <div className="absolute -inset-16 animate-pulse rounded-full border border-red-400/[0.08]" />

                  <div className="absolute -inset-9 rounded-full border border-red-400/20" />

                  <div className="relative flex h-14 w-14 items-center justify-center rounded-full border border-red-400/40 bg-red-400/[0.08] text-red-300 shadow-[0_0_50px_rgba(248,113,113,.18)]">

                    <Icon
                      name="alert"
                      size={23}
                    />

                  </div>

                  <p className="mt-3 whitespace-nowrap text-center text-[10px] font-bold uppercase tracking-[0.22em] text-red-300">
                    Incident zone
                  </p>

                </div>

                {/* map controls */}

                <div className="absolute bottom-5 left-5 flex items-center gap-2">

                  <MapInfo
                    label="Coverage"
                    value="10.0 km"
                  />

                  <MapInfo
                    label="Fleet"
                    value={`${activeDrones} active`}
                  />

                </div>

                <div className="absolute bottom-5 right-5 rounded-xl border border-white/[0.07] bg-[#03060b]/80 px-4 py-3 backdrop-blur-xl">

                  <div className="flex items-center gap-4 text-[10px]">

                    <span className="flex items-center gap-2 text-slate-500">
                      <StatusDot />
                      Available
                    </span>

                    <span className="flex items-center gap-2 text-slate-500">
                      <StatusDot type="warning" />
                      Inspecting
                    </span>

                    <span className="flex items-center gap-2 text-slate-500">
                      <StatusDot type="danger" />
                      Incident
                    </span>

                  </div>

                </div>

              </div>

              {/* FLEET */}

              <div className="rounded-[22px] border border-white/[0.09] bg-[#070d15]/90 shadow-[0_30px_100px_rgba(0,0,0,.3)] backdrop-blur-xl">

                <div className="border-b border-white/[0.06] px-6 py-5">

                  <p className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-300">
                    Fleet telemetry
                  </p>

                  <p className="mt-1.5 text-xs text-slate-600">
                    Live vehicle availability
                  </p>

                </div>

                <div className="divide-y divide-white/[0.05]">

                  {drones.map(
                    (drone) => (
                      <DroneRow
                        key={drone.id}
                        drone={drone}
                      />
                    )
                  )}

                  {!drones.length && (
                    <div className="p-8 text-sm text-slate-600">
                      Synchronizing fleet…
                    </div>
                  )}

                </div>

                <div className="border-t border-white/[0.06] px-6 py-5">

                  <div className="flex items-center justify-between">

                    <span className="text-xs text-slate-600">
                      Fleet readiness
                    </span>

                    <span className="text-sm font-semibold text-emerald-300">
                      {averageBattery}%
                    </span>

                  </div>

                  <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-white/[0.05]">

                    <div
                      className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-cyan-400 transition-all duration-700"
                      style={{
                        width: `${averageBattery}%`,
                      }}
                    />

                  </div>

                  <div className="mt-4 flex justify-between text-[10px] text-slate-700">

                    <span>
                      3 vehicles registered
                    </span>

                    <span>
                      Auto-refresh 3s
                    </span>

                  </div>

                </div>

              </div>

            </section>

            {/* =================================================
                RESPONSE + INTELLIGENCE
            ================================================= */}

            <section className="mb-6 grid gap-6 xl:grid-cols-[1fr_1.3fr]">

              {/* RESPONSE */}

              <div className="rounded-[22px] border border-white/[0.09] bg-[#070d15]/90 p-6 shadow-[0_30px_100px_rgba(0,0,0,.3)] backdrop-blur-xl">

                <div className="flex items-start justify-between">

                  <div>

                    <p className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-300">
                      Initiate response
                    </p>

                    <p className="mt-1.5 text-xs text-slate-600">
                      Dispatch autonomous emergency mission
                    </p>

                  </div>

                  <span className="rounded-lg border border-white/[0.07] px-3 py-1.5 text-[10px] font-semibold uppercase tracking-wider text-slate-600">
                    Controlled
                  </span>

                </div>

                <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3">

                  {INCIDENTS.map(
                    (item) => {

                      const selected =
                        incident === item.id;

                      return (
                        <button
                          key={item.id}
                          disabled={
                            triggering
                          }
                          onClick={() =>
                            setIncident(
                              item.id
                            )
                          }
                          className={`group rounded-xl border p-4 text-left transition duration-200 ${
                            selected
                              ? "border-cyan-400/40 bg-cyan-400/[0.07] shadow-[0_0_30px_rgba(34,211,238,.05)]"
                              : "border-white/[0.07] bg-white/[0.015] hover:-translate-y-0.5 hover:border-white/[0.15] hover:bg-white/[0.035]"
                          }`}
                        >

                          <div className="flex items-center justify-between">

                            <span
                              className={`text-lg ${
                                selected
                                  ? "opacity-100"
                                  : "opacity-40 grayscale"
                              }`}
                            >
                              {item.icon}
                            </span>

                            {selected && (
                              <StatusDot
                                type="blue"
                              />
                            )}

                          </div>

                          <p
                            className={`mt-3 text-sm font-medium ${
                              selected
                                ? "text-cyan-200"
                                : "text-slate-300"
                            }`}
                          >
                            {item.label}
                          </p>

                          <p className="mt-1 text-xs text-slate-600">
                            {item.sub}
                          </p>

                        </button>
                      );
                    }
                  )}

                </div>

                <div className="mt-5 rounded-xl border border-white/[0.07] bg-white/[0.018] p-4">

                  <div className="flex items-center justify-between">

                    <div>

                      <p className="text-[10px] uppercase tracking-[0.18em] text-slate-600">
                        Selected incident
                      </p>

                      <p className="mt-1.5 text-base font-medium capitalize">
                        {incident.replaceAll(
                          "_",
                          " "
                        )}
                      </p>

                      <p className="mt-1 font-mono text-[10px] text-slate-700">
                        17.6868° N · 83.2185° E
                      </p>

                    </div>

                    <button
                      onClick={
                        triggerEmergency
                      }
                      disabled={
                        triggering ||
                        !connected
                      }
                      className="rounded-xl bg-cyan-400 px-5 py-3 text-xs font-bold uppercase tracking-wide text-[#031017] shadow-[0_0_25px_rgba(34,211,238,.08)] transition hover:bg-cyan-300 hover:shadow-[0_0_40px_rgba(34,211,238,.18)] disabled:cursor-not-allowed disabled:bg-slate-800 disabled:text-slate-600"
                    >
                      {triggering
                        ? "Dispatching…"
                        : "Initiate response"}
                    </button>

                  </div>

                </div>

                {result && (
                  <div
                    className={`mt-5 rounded-xl border p-4 ${
                      result.error
                        ? "border-red-400/20 bg-red-400/[0.04]"
                        : result.approval ||
                            result.status ===
                              "human_review_required"
                          ? "border-amber-400/20 bg-amber-400/[0.04]"
                          : "border-emerald-400/20 bg-emerald-400/[0.04]"
                    }`}
                  >

                    <div className="flex items-center gap-2">

                      <StatusDot
                        type={
                          result.error
                            ? "danger"
                            : result.approval ||
                                result.status ===
                                  "human_review_required"
                              ? "warning"
                              : "success"
                        }
                      />

                      <p className="text-sm font-semibold">
                        {result.error
                          ? "Mission failed"
                          : result.approval ||
                              result.status ===
                                "human_review_required"
                            ? "Operator authorization required"
                            : "Mission accepted"}
                      </p>

                    </div>

                    <p className="mt-2 text-xs text-slate-500">
                      {result.error ||
                        result.mission_id ||
                        result.status}
                    </p>

                  </div>
                )}

              </div>

              {/* INTELLIGENCE */}

              <div className="rounded-[22px] border border-white/[0.09] bg-[#070d15]/90 p-6 shadow-[0_30px_100px_rgba(0,0,0,.3)] backdrop-blur-xl">

                <div className="flex items-start justify-between">

                  <div>

                    <p className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-300">
                      Autonomous intelligence
                    </p>

                    <p className="mt-1.5 font-mono text-xs text-slate-600">
                      {latestMission?.mission_id ||
                        "NO ACTIVE MISSION"}
                    </p>

                  </div>

                  {latestMission && (
                    <div
                      className={`rounded-full px-3 py-1.5 text-[10px] font-semibold uppercase tracking-wider ${
                        needsApproval
                          ? "bg-amber-400/10 text-amber-300"
                          : missionCompleted
                            ? "bg-emerald-400/10 text-emerald-300"
                            : "bg-cyan-400/10 text-cyan-300"
                      }`}
                    >
                      {needsApproval
                        ? "Human review"
                        : missionCompleted
                          ? "Completed"
                          : "Active"}
                    </div>
                  )}

                </div>

                <div className="mt-6 grid gap-5 lg:grid-cols-[1.15fr_.85fr]">

                  {/* PIPELINE */}

                  <div className="rounded-xl border border-white/[0.07] bg-white/[0.015] p-5">

                    <div className="flex items-center justify-between">

                      <p className="text-[10px] font-semibold uppercase tracking-[0.22em] text-slate-600">
                        Decision engine
                      </p>

                      <span className="font-mono text-[10px] text-cyan-400">
                        AGENT GRAPH
                      </span>

                    </div>

                    <div className="mt-5 space-y-1">

                      <Pipeline
                        n="01"
                        title="Incident"
                        value={
                          latestMission
                            ? latestMission.incident_type
                            : "Awaiting signal"
                        }
                        active={
                          !!latestMission
                        }
                      />

                      <Pipeline
                        n="02"
                        title="Fleet selection"
                        value={
                          latestMission
                            ? `${latestMission.drone_id} selected`
                            : "Awaiting selection"
                        }
                        active={
                          !!latestMission
                        }
                      />

                      <Pipeline
                        n="03"
                        title="Knowledge retrieval"
                        value={
                          latestMission
                            ? knowledgeSource(
                                latestMission.incident_type
                              )
                            : "RAG pending"
                        }
                        active={
                          !!latestMission
                        }
                      />

                      <Pipeline
                        n="04"
                        title="Vision analysis"
                        value={
                          latestAnalysis
                            ? `${Math.round(
                                latestAnalysis.confidence *
                                  100
                              )}% confidence`
                            : "Awaiting evidence"
                        }
                        active={
                          !!latestAnalysis
                        }
                      />

                      <Pipeline
                        n="05"
                        title="Decision"
                        value={
                          latestDecision
                            ? formatDecision(
                                latestDecision.decision
                              )
                            : "Awaiting decision"
                        }
                        active={
                          !!latestDecision
                        }
                      />

                      <Pipeline
                        n="06"
                        title="Safety Governor"
                        value={
                          needsApproval
                            ? "Autonomy paused"
                            : latestMission
                              ? "Checks passed"
                              : "Awaiting action"
                        }
                        active={
                          !!latestMission
                        }
                        warning={
                          needsApproval
                        }
                      />

                    </div>

                  </div>

                  {/* ASSESSMENT */}

                  <div
                    className={`rounded-xl border p-5 ${
                      needsApproval
                        ? "border-amber-400/20 bg-amber-400/[0.035]"
                        : "border-white/[0.07] bg-white/[0.015]"
                    }`}
                  >

                    <p className="text-[10px] font-semibold uppercase tracking-[0.22em] text-slate-600">
                      Current assessment
                    </p>

                    <div className="mt-6 flex items-end justify-between">

                      <div>

                        <p className="text-6xl font-semibold tracking-[-0.05em]">
                          {latestAnalysis?.confidence !=
                          null
                            ? `${Math.round(
                                latestAnalysis.confidence *
                                  100
                              )}%`
                            : "—"}
                        </p>

                        <p className="mt-2 text-xs text-slate-600">
                          Vision confidence
                        </p>

                      </div>

                      <div className="flex h-14 w-14 items-center justify-center rounded-full border border-cyan-400/10 bg-cyan-400/[0.03] text-cyan-300">

                        <Icon
                          name="brain"
                          size={21}
                        />

                      </div>

                    </div>

                    <div className="mt-7 border-t border-white/[0.06] pt-5">

                      <p className="text-[10px] uppercase tracking-[0.18em] text-slate-600">
                        Recommended action
                      </p>

                      <p className="mt-3 text-sm leading-6 text-slate-400">
                        {latestAnalysis?.recommended_action ||
                          "Awaiting aerial evidence from the active mission."}
                      </p>

                    </div>

                  </div>

                </div>

              </div>

            </section>

            {/* =================================================
                HUMAN APPROVAL
            ================================================= */}

            {approvals.length > 0 && (

              <section className="relative mb-6 overflow-hidden rounded-[22px] border border-amber-400/25 bg-[#0c0e0c] shadow-[0_30px_100px_rgba(251,191,36,.05)]">

                <div className="absolute inset-0 bg-[radial-gradient(circle_at_10%_50%,rgba(251,191,36,.06),transparent_35%)]" />

                <div className="relative flex flex-col justify-between gap-5 border-b border-amber-400/10 bg-amber-400/[0.025] px-6 py-5 sm:flex-row sm:items-center">

                  <div className="flex items-center gap-4">

                    <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-amber-400/20 bg-amber-400/[0.07] text-amber-300">

                      <Icon
                        name="shield"
                        size={21}
                      />

                    </div>

                    <div>

                      <div className="flex items-center gap-2">

                        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-amber-300">
                          Human authorization required
                        </p>

                        <StatusDot
                          type="warning"
                          pulse
                        />

                      </div>

                      <p className="mt-1.5 text-xs text-slate-600">
                        Safety Governor has paused autonomous continuation.
                      </p>

                    </div>

                  </div>

                  <span className="rounded-full bg-amber-400/10 px-3 py-1.5 text-[10px] font-semibold text-amber-300">
                    {approvals.length} PENDING
                  </span>

                </div>

                <div className="relative">

                  {approvals.map(
                    (approval) => {

                      const request =
                        approval.request ||
                        approval;

                      const busy =
                        busyMission ===
                        request.mission_id;

                      return (
                        <div
                          key={
                            request.mission_id
                          }
                          className="p-6"
                        >

                          <div className="grid gap-7 lg:grid-cols-[1fr_auto] lg:items-center">

                            <div>

                              <div className="grid gap-5 sm:grid-cols-4">

                                <Approval
                                  label="Mission"
                                  value={
                                    request.mission_id
                                  }
                                />

                                <Approval
                                  label="Vehicle"
                                  value={
                                    request.drone_id
                                  }
                                />

                                <Approval
                                  label="Action"
                                  value={
                                    request.action
                                  }
                                />

                                <Approval
                                  label="Risk"
                                  value={
                                    request.risk_level
                                  }
                                  warning
                                />

                              </div>

                              <div className="mt-5 rounded-xl border border-white/[0.06] bg-black/20 p-4">

                                <p className="text-[10px] uppercase tracking-[0.18em] text-slate-700">
                                  Safety rationale
                                </p>

                                <p className="mt-2 text-sm leading-6 text-slate-400">
                                  {request.reason}
                                </p>

                              </div>

                            </div>

                            <div className="flex gap-3 lg:flex-col">

                              <button
                                disabled={busy}
                                onClick={() =>
                                  resolveApproval(
                                    request.mission_id,
                                    false
                                  )
                                }
                                className="rounded-xl border border-red-400/20 px-5 py-3.5 text-xs font-semibold uppercase tracking-wide text-red-300 transition hover:bg-red-400/[0.05] disabled:opacity-50"
                              >
                                {busy
                                  ? "Processing…"
                                  : "Reject & return"}
                              </button>

                              <button
                                disabled={busy}
                                onClick={() =>
                                  resolveApproval(
                                    request.mission_id,
                                    true
                                  )
                                }
                                className="rounded-xl bg-emerald-400 px-6 py-3.5 text-xs font-bold uppercase tracking-wide text-[#031017] shadow-[0_0_30px_rgba(52,211,153,.08)] transition hover:bg-emerald-300 hover:shadow-[0_0_40px_rgba(52,211,153,.15)] disabled:opacity-50"
                              >
                                {busy
                                  ? "Processing…"
                                  : "Authorize mission"}
                              </button>

                            </div>

                          </div>

                        </div>
                      );
                    }
                  )}

                </div>

              </section>

            )}

            {/* =================================================
                MISSION LEDGER
            ================================================= */}

            <section className="overflow-hidden rounded-[22px] border border-white/[0.09] bg-[#070d15]/90 shadow-[0_30px_100px_rgba(0,0,0,.25)] backdrop-blur-xl">

              <div className="flex items-center justify-between border-b border-white/[0.06] px-6 py-5">

                <div>

                  <p className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-300">
                    Mission ledger
                  </p>

                  <p className="mt-1.5 text-xs text-slate-600">
                    Persistent operational history
                  </p>

                </div>

                <span className="rounded-lg border border-white/[0.06] px-3 py-1.5 text-[10px] text-slate-600">
                  {missions.length} records
                </span>

              </div>

              <div className="overflow-x-auto">

                <table className="w-full min-w-[850px]">

                  <thead>

                    <tr className="border-b border-white/[0.05] text-left text-[10px] uppercase tracking-[0.2em] text-slate-700">

                      <th className="px-6 py-4">
                        Mission
                      </th>

                      <th className="py-4">
                        Incident
                      </th>

                      <th className="py-4">
                        Vehicle
                      </th>

                      <th className="py-4">
                        Confidence
                      </th>

                      <th className="py-4">
                        Status
                      </th>

                      <th className="px-6 py-4">
                        Time
                      </th>

                    </tr>

                  </thead>

                  <tbody>

                    {missions
                      .slice(0, 10)
                      .map(
                        (mission) => (
                          <MissionRow
                            key={
                              mission.mission_id
                            }
                            mission={
                              mission
                            }
                          />
                        )
                      )}

                  </tbody>

                </table>

                {!missions.length && (
                  <div className="px-6 py-14 text-center text-sm text-slate-700">
                    No missions recorded.
                  </div>
                )}

              </div>

            </section>

            {/* FOOTER */}

            <footer className="flex flex-col gap-3 border-t border-white/[0.05] py-7 text-[10px] uppercase tracking-[0.15em] text-slate-700 sm:flex-row sm:items-center sm:justify-between">

              <span>
                DroneRescue · Autonomous Response Infrastructure
              </span>

              <div className="flex flex-wrap gap-5">

                <span>
                  API{" "}
                  {connected
                    ? "CONNECTED"
                    : "DISCONNECTED"}
                </span>

                <span>
                  RAG READY
                </span>

                <span>
                  VISION READY
                </span>

                <span>
                  SAFETY ACTIVE
                </span>

                <span>
                  HITL ENABLED
                </span>

              </div>

            </footer>

          </div>

        </main>

      </div>

      {/* =====================================================
          ANIMATION
      ===================================================== */}

      <style>{`

        @keyframes spin {
          from {
            transform: rotate(0deg);
          }

          to {
            transform: rotate(360deg);
          }
        }

      `}</style>

    </div>
  );
}

/* =========================================================
   COMPONENTS
========================================================= */

function SmallSystem({
  label,
  value,
}) {
  return (
    <div>

      <p className="text-[9px] uppercase tracking-wider text-slate-700">
        {label}
      </p>

      <p className="mt-1 text-[10px] font-semibold text-emerald-400">
        {value}
      </p>

    </div>
  );
}

function KPI({
  label,
  value,
}) {
  return (
    <div className="min-w-[100px] px-6 py-4">

      <p className="text-[10px] uppercase tracking-[0.15em] text-slate-600">
        {label}
      </p>

      <p className="mt-1 text-2xl font-semibold tracking-tight">
        {value}
      </p>

    </div>
  );
}

function MapDrone({
  id,
  name,
  left,
  top,
  active = false,
}) {
  return (
    <div
      className="absolute -translate-x-1/2 -translate-y-1/2"
      style={{
        left,
        top,
      }}
    >

      {active && (
        <div className="absolute -inset-4 animate-ping rounded-full border border-cyan-400/20" />
      )}

      <div
        className={`relative flex h-11 w-11 items-center justify-center rounded-full border ${
          active
            ? "border-cyan-400/45 bg-cyan-400/10 text-cyan-300 shadow-[0_0_30px_rgba(34,211,238,.14)]"
            : "border-white/[0.14] bg-slate-700/20 text-slate-400"
        }`}
      >

        <Icon
          name="drone"
          size={18}
        />

        <span
          className={`absolute right-0 top-0 h-2 w-2 rounded-full ${
            active
              ? "bg-cyan-300"
              : "bg-emerald-400"
          }`}
        />

      </div>

      <div className="mt-2 text-center">

        <p className="font-mono text-[10px] text-slate-400">
          {id}
        </p>

        <p className="mt-0.5 whitespace-nowrap text-[9px] text-slate-700">
          {name}
        </p>

      </div>

    </div>
  );
}

function MapInfo({
  label,
  value,
}) {
  return (
    <div className="rounded-xl border border-white/[0.07] bg-[#03060b]/80 px-4 py-3 backdrop-blur-xl">

      <p className="text-[9px] uppercase tracking-wider text-slate-700">
        {label}
      </p>

      <p className="mt-1 font-mono text-xs text-slate-300">
        {value}
      </p>

    </div>
  );
}

function DroneRow({
  drone,
}) {

  const active =
    drone.status === "flying" ||
    drone.status === "inspecting";

  return (
    <div className="px-6 py-5 transition hover:bg-white/[0.018]">

      <div className="flex items-center gap-4">

        <div
          className={`flex h-11 w-11 items-center justify-center rounded-xl ${
            active
              ? "bg-amber-400/[0.08] text-amber-300"
              : "bg-white/[0.035] text-slate-400"
          }`}
        >

          <Icon
            name="drone"
            size={19}
          />

        </div>

        <div className="min-w-0 flex-1">

          <div className="flex items-center gap-2">

            <p className="truncate text-sm font-medium">
              {drone.name}
            </p>

            <span className="font-mono text-[10px] text-slate-700">
              {drone.id}
            </span>

          </div>

          <p className="mt-1 text-[10px] uppercase tracking-wider text-slate-600">
            {drone.capabilities?.thermal_camera
              ? "RGB · THERMAL"
              : "RGB"}
          </p>

        </div>

        <div className="text-right">

          <div className="flex items-center justify-end gap-2">

            <StatusDot
              type={
                active
                  ? "warning"
                  : "success"
              }
            />

            <span className="text-[10px] font-medium uppercase text-slate-500">
              {drone.status}
            </span>

          </div>

          <p className="mt-1 text-sm font-semibold">
            {Math.round(
              drone.battery
            )}
            %
          </p>

        </div>

      </div>

      <div className="mt-4 h-1 overflow-hidden rounded-full bg-white/[0.05]">

        <div
          className="h-full rounded-full bg-slate-500 transition-all duration-700"
          style={{
            width: `${drone.battery}%`,
          }}
        />

      </div>

    </div>
  );
}

function Pipeline({
  n,
  title,
  value,
  active,
  warning,
}) {
  return (
    <div className="group flex items-center gap-4 rounded-xl px-3 py-3 transition hover:bg-white/[0.025]">

      <span
        className={`font-mono text-[10px] ${
          warning
            ? "text-amber-400"
            : active
              ? "text-cyan-400"
              : "text-slate-700"
        }`}
      >
        {n}
      </span>

      <div className="h-px w-5 bg-white/[0.06]" />

      <div className="min-w-0 flex-1">

        <p className="text-sm font-medium text-slate-300">
          {title}
        </p>

        <p className="mt-1 truncate text-xs capitalize text-slate-600">
          {String(value).replaceAll(
            "_",
            " "
          )}
        </p>

      </div>

      <StatusDot
        type={
          warning
            ? "warning"
            : active
              ? "success"
              : "blue"
        }
      />

    </div>
  );
}

function Approval({
  label,
  value,
  warning = false,
}) {
  return (
    <div>

      <p className="text-[10px] uppercase tracking-[0.18em] text-slate-700">
        {label}
      </p>

      <p
        className={`mt-1.5 font-mono text-sm ${
          warning
            ? "text-amber-300"
            : "text-slate-300"
        }`}
      >
        {value || "—"}
      </p>

    </div>
  );
}

function MissionRow({
  mission,
}) {

  const observations =
    mission.observations || [];

  const confidence =
    observations
      .map(
        (item) =>
          item.analysis?.confidence
      )
      .filter(
        (value) =>
          typeof value === "number"
      );

  let confidenceText = "—";

  if (confidence.length === 1) {

    confidenceText =
      `${Math.round(
        confidence[0] * 100
      )}%`;

  } else if (confidence.length > 1) {

    confidenceText =
      `${Math.round(
        confidence[0] * 100
      )}% → ${Math.round(
        confidence[
          confidence.length - 1
        ] * 100
      )}%`;

  }

  const status =
    mission.status?.toUpperCase() ||
    "UNKNOWN";

  const completed =
    status ===
      "MISSION_COMPLETED" ||
    status === "COMPLETED";

  const review =
    status ===
    "HUMAN_REVIEW_REQUIRED";

  const failed =
    status === "MISSION_FAILED" ||
    status === "SAFETY_BLOCKED" ||
    status === "RETURN_FAILED";

  let type = "warning";
  let text = status;

  if (completed) {
    type = "success";
    text = "Completed";
  } else if (review) {
    type = "warning";
    text = "Human review";
  } else if (failed) {
    type = "danger";
    text = "Failed";
  }

  return (
    <tr className="border-b border-white/[0.04] text-sm transition hover:bg-white/[0.018]">

      <td className="px-6 py-5 font-mono text-[11px] text-cyan-300">
        {mission.mission_id}
      </td>

      <td className="py-5 capitalize text-slate-300">
        {mission.incident_type?.replaceAll(
          "_",
          " "
        )}
      </td>

      <td className="py-5 font-mono text-slate-500">
        {mission.drone_id}
      </td>

      <td className="py-5 text-slate-400">
        {confidenceText}
      </td>

      <td className="py-5">

        <span
          className={`inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-[10px] font-semibold uppercase tracking-wider ${
            type === "success"
              ? "bg-emerald-400/10 text-emerald-300"
              : type === "danger"
                ? "bg-red-400/10 text-red-300"
                : "bg-amber-400/10 text-amber-300"
          }`}
        >

          <StatusDot
            type={type}
          />

          {text}

        </span>

      </td>

      <td className="px-6 py-5 text-slate-600">

        {mission.created_at
          ? new Date(
              mission.created_at
            ).toLocaleTimeString(
              [],
              {
                hour: "2-digit",
                minute: "2-digit",
              }
            )
          : "—"}

      </td>

    </tr>
  );
}

/* =========================================================
   HELPERS
========================================================= */

function knowledgeSource(
  incident
) {

  if (incident === "fire") {
    return "Fire protocol";
  }

  if (
    incident === "intrusion"
  ) {
    return "Security protocol";
  }

  return "Emergency response";
}

function formatDecision(
  decision
) {

  const labels = {

    thermal_inspection:
      "Thermal inspection",

    remote_hazard_inspection:
      "Remote hazard inspection",

    aerial_surveillance:
      "Aerial surveillance",

    scene_assessment:
      "Scene assessment",

    structural_inspection:
      "Structural inspection",

    flood_mapping:
      "Flood mapping",

    recapture:
      "Replan · recapture",

    continue_monitoring:
      "Continue monitoring",

    human_approved_continuation:
      "Human authorization",

  };

  return (
    labels[decision] ||
    decision ||
    "Awaiting"
  );
}