function Header({ logout }) {
  return (
    <header className="flex items-center justify-between border-b border-slate-700 px-8 py-5">

      <h1 className="text-2xl font-bold">
        ⚡ SynapseOS
      </h1>

      <button
        onClick={logout}
        className="rounded-lg bg-red-500 px-4 py-2 hover:bg-red-600"
      >
        Logout
      </button>

    </header>
  );
}

export default Header;