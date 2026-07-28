function Header({ logout }) {
  return (
    <header className="flex items-center justify-between border-b border-slate-800 bg-slate-950 px-8 py-5">

      <div>
        <h1 className="text-2xl font-bold text-white">
          ⚡ SynapseOS
        </h1>

        <p className="text-sm text-slate-400">
          AI Operating System
        </p>
      </div>

      <button
        onClick={logout}
        className="rounded-lg bg-red-500 px-4 py-2 text-white transition hover:bg-red-600"
      >
        Logout
      </button>

    </header>
  );
}

export default Header;