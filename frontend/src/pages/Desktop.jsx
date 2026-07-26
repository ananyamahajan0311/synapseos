import { useNavigate } from "react-router-dom";
import "../App.css";

function Desktop() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
  <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 text-white">

    {/* Header */}
    <header className="flex items-center justify-between px-8 py-6 border-b border-white/10">
      <h1 className="text-2xl font-bold">⚡ SynapseOS</h1>

      <button
        onClick={logout}
        className="rounded-lg bg-red-500 px-4 py-2 font-semibold transition hover:bg-red-600"
      >
        Logout
      </button>
    </header>

    {/* Main */}
    <main className="mx-auto flex max-w-4xl flex-col items-center px-6 py-16">

      <h2 className="text-center text-5xl font-extrabold tracking-tight">
        Tell it. It gets done.
      </h2>

      <p className="mt-4 text-lg text-slate-300">
        What would you like me to do today?
      </p>

      <div className="mt-10 w-full rounded-2xl border border-slate-700 bg-slate-900/70 p-5 shadow-xl backdrop-blur">

        <textarea
          rows={8}
          placeholder={`Type anything...

Example:
Write an apology email to my professor.
Create an attendance sheet.
Schedule tomorrow's AI Lab.`}
          className="w-full resize-none bg-transparent text-white placeholder:text-slate-500 focus:outline-none"
        />

        <div className="mt-4 flex justify-end">
          <button className="rounded-xl bg-indigo-600 px-6 py-3 font-semibold transition hover:bg-indigo-700">
            Send →
          </button>
        </div>

      </div>

    </main>

  </div>
);
}

export default Desktop;