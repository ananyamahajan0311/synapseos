const styles = {
  bar: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "14px 28px",
    background: "#FDFCFBcc",
    backdropFilter: "blur(10px)",
    borderBottom: "1px solid #E3DAF4",
  },
  logoWrap: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
  },
  logoMark: {
    width: "38px",
    height: "38px",
    borderRadius: "12px",
    background: "linear-gradient(135deg, #A79AE8, #8B7BDC)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "18px",
    boxShadow: "0 6px 14px -6px rgba(124,109,216,0.6)",
  },
  logoText: {
    fontFamily: "'Baloo 2', sans-serif",
    fontSize: "18px",
    fontWeight: 700,
    color: "#4A3F6B",
    margin: 0,
  },
  logoSub: {
    fontSize: "11px",
    color: "#9B92B3",
    fontWeight: 700,
    margin: 0,
  },
  logoutBtn: {
    height: "38px",
    padding: "0 18px",
    borderRadius: "19px",
    border: "1.5px solid #E3DAF4",
    background: "#fff",
    color: "#8B7BDC",
    fontFamily: "'Nunito', sans-serif",
    fontWeight: 800,
    fontSize: "13px",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    gap: "6px",
    transition: "background 0.15s, transform 0.12s, color 0.15s",
  },
};

export default function Header({ logout }) {
  return (
    <div style={styles.bar}>
      <div style={styles.logoWrap}>
        <div style={styles.logoMark}>⚡</div>
        <div>
          <p style={styles.logoText}>SynapseOS</p>
          <p style={styles.logoSub}>your friendly assistant</p>
        </div>
      </div>

      <button
        className="header-logout-btn"
        style={styles.logoutBtn}
        onClick={logout}
      >
        Log out ↩
      </button>

      <style>{`
        .header-logout-btn:hover {
          background: #F7F4FC !important;
          border-color: #C9BFEA !important;
          transform: translateY(-1px);
        }
        .header-logout-btn:active {
          transform: scale(0.97) !important;
        }
      `}</style>
    </div>
  );
}