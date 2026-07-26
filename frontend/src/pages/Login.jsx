import { useState } from "react";
import { useNavigate } from "react-router-dom";

const styles = {
  wrap: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#0f0f13",
    fontFamily: "'DM Sans', sans-serif",
    padding: "2rem 1rem",
  },
  card: {
    width: "100%",
    maxWidth: "400px",
    background: "#16161d",
    border: "1px solid #2a2a38",
    borderRadius: "24px",
    padding: "2.5rem 2rem",
    position: "relative",
    overflow: "hidden",
  },
  glowTop: {
    position: "absolute",
    width: "220px",
    height: "220px",
    borderRadius: "50%",
    background: "radial-gradient(circle, #7F77DD33 0%, transparent 70%)",
    top: "-80px",
    right: "-60px",
    pointerEvents: "none",
  },
  glowBottom: {
    position: "absolute",
    width: "180px",
    height: "180px",
    borderRadius: "50%",
    background: "radial-gradient(circle, #5DCAA522 0%, transparent 70%)",
    bottom: "-60px",
    left: "-40px",
    pointerEvents: "none",
  },
  logo: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    marginBottom: "2rem",
  },
  logoMark: {
    width: "36px",
    height: "36px",
    borderRadius: "10px",
    background: "linear-gradient(135deg, #7F77DD, #5DCAA5)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "18px",
  },
  logoText: {
    fontFamily: "'Syne', sans-serif",
    fontSize: "18px",
    fontWeight: 800,
    color: "#fff",
    letterSpacing: "-0.5px",
  },
  pill: {
    display: "inline-flex",
    alignItems: "center",
    gap: "5px",
    background: "#7F77DD1a",
    color: "#a09ae8",
    fontSize: "11px",
    fontWeight: 500,
    padding: "3px 9px",
    borderRadius: "20px",
    marginBottom: "1.25rem",
    border: "1px solid #7F77DD33",
  },
  title: {
    fontFamily: "'Syne', sans-serif",
    fontSize: "26px",
    fontWeight: 800,
    color: "#fff",
    margin: "0 0 6px",
    letterSpacing: "-0.5px",
  },
  sub: {
    fontSize: "14px",
    color: "#666",
    margin: "0 0 2rem",
  },
  label: {
    display: "block",
    fontSize: "11px",
    fontWeight: 500,
    color: "#555",
    letterSpacing: "0.07em",
    textTransform: "uppercase",
    marginBottom: "6px",
  },
  fieldWrap: {
    position: "relative",
    marginBottom: "1.25rem",
  },
  fieldIcon: {
    position: "absolute",
    left: "12px",
    top: "50%",
    transform: "translateY(-50%)",
    fontSize: "16px",
    color: "#444",
    pointerEvents: "none",
    zIndex: 1,
  },
  input: {
    width: "100%",
    height: "44px",
    padding: "0 12px 0 38px",
    borderRadius: "12px",
    border: "1px solid #2a2a38",
    background: "#1c1c26",
    fontSize: "14px",
    fontFamily: "'DM Sans', sans-serif",
    color: "#e0e0e0",
    outline: "none",
    boxSizing: "border-box",
    transition: "border-color 0.15s, box-shadow 0.15s",
  },
  forgot: {
    display: "block",
    textAlign: "right",
    fontSize: "12px",
    color: "#7F77DD",
    textDecoration: "none",
    marginTop: "-0.75rem",
    marginBottom: "1.5rem",
    cursor: "pointer",
    background: "none",
    border: "none",
  },
  btn: {
    width: "100%",
    height: "46px",
    borderRadius: "12px",
    border: "none",
    background: "linear-gradient(135deg, #7F77DD, #5DCAA5)",
    color: "#fff",
    fontFamily: "'Syne', sans-serif",
    fontSize: "15px",
    fontWeight: 700,
    letterSpacing: "0.02em",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "8px",
    transition: "transform 0.12s, opacity 0.12s",
    position: "relative",
    overflow: "hidden",
  },
  dividerWrap: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    margin: "1.5rem 0",
  },
  dividerLine: {
    flex: 1,
    height: "1px",
    background: "#2a2a38",
  },
  dividerText: {
    fontSize: "12px",
    color: "#444",
    whiteSpace: "nowrap",
  },
  socialRow: {
    display: "flex",
    gap: "10px",
  },
  socialBtn: {
    flex: 1,
    height: "40px",
    borderRadius: "10px",
    border: "1px solid #2a2a38",
    background: "#1c1c26",
    color: "#888",
    fontSize: "13px",
    fontFamily: "'DM Sans', sans-serif",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "7px",
    transition: "background 0.12s, border-color 0.12s",
  },
  signupRow: {
    textAlign: "center",
    marginTop: "1.5rem",
    fontSize: "13px",
    color: "#555",
  },
  signupLink: {
    color: "#7F77DD",
    textDecoration: "none",
    fontWeight: 500,
  },
};

// Inject Google Fonts + keyframes once
const injectFonts = () => {
  if (document.getElementById("login-fonts")) return;
  const link = document.createElement("link");
  link.id = "login-fonts";
  link.rel = "stylesheet";
  link.href =
    "https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap";
  document.head.appendChild(link);

  const tablerLink = document.createElement("link");
  tablerLink.rel = "stylesheet";
  tablerLink.href =
    "https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css";
  document.head.appendChild(tablerLink);

  const styleEl = document.createElement("style");
  styleEl.textContent = `
    @keyframes shine {
      0% { left: -100%; }
      40% { left: 120%; }
      100% { left: 120%; }
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    .login-input:focus {
      border-color: #7F77DD !important;
      box-shadow: 0 0 0 3px #7F77DD22 !important;
    }
    .login-social-btn:hover {
      background: #222230 !important;
      border-color: #3a3a50 !important;
      color: #bbb !important;
    }
    .login-btn:hover {
      transform: translateY(-1px);
      opacity: 0.92;
    }
    .login-btn:active {
      transform: scale(0.98) !important;
    }
    .btn-shine {
      position: absolute;
      top: 0;
      left: -100%;
      width: 60%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
      animation: shine 2.4s infinite;
    }
  `;
  document.head.appendChild(styleEl);
};

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [btnState, setBtnState] = useState("idle"); // idle | loading | success | error
  const navigate = useNavigate();

  injectFonts();

  const getBtnStyle = () => {
    const base = { ...styles.btn };
    if (btnState === "error")
      base.background = "linear-gradient(135deg, #E24B4A, #D85A30)";
    if (btnState === "success")
      base.background = "linear-gradient(135deg, #1D9E75, #3B6D11)";
    return base;
  };

  const getBtnContent = () => {
    if (btnState === "loading")
      return (
        <>
          <span className="btn-shine" />
          <i
            className="ti ti-loader-2"
            style={{ fontSize: 18, animation: "spin 0.8s linear infinite" }}
          />
          Signing in…
        </>
      );
    if (btnState === "success")
      return (
        <>
          <span className="btn-shine" />
          <i className="ti ti-circle-check" style={{ fontSize: 18 }} />
          Success!
        </>
      );
    if (btnState === "error")
      return (
        <>
          <span className="btn-shine" />
          <i className="ti ti-alert-circle" style={{ fontSize: 18 }} />
          Check your details
        </>
      );
    return (
      <>
        <span className="btn-shine" />
        <i className="ti ti-login" style={{ fontSize: 18 }} />
        Sign in
      </>
    );
  };

  const login = async () => {
    if (!email || !password) {
      setBtnState("error");
      setTimeout(() => setBtnState("idle"), 2000);
      return;
    }
    setBtnState("loading");
    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        setBtnState("success");
        setTimeout(() => navigate("/dashboard"), 800);
      } else {
        setBtnState("error");
        setTimeout(() => setBtnState("idle"), 2000);
      }
    } catch {
      setBtnState("error");
      setTimeout(() => setBtnState("idle"), 2000);
    }
  };

  return (
    <div style={styles.wrap}>
      <div style={styles.card}>
        <div style={styles.glowTop} />
        <div style={styles.glowBottom} />

        {/* Logo */}
        <div style={styles.logo}>
          <div style={styles.logoMark}>⚡</div>
          <span style={styles.logoText}>Nexus</span>
        </div>

        {/* Badge */}
        <div style={styles.pill}>🔒 Secure login</div>

        <h1 style={styles.title}>Welcome back</h1>
        <p style={styles.sub}>Sign in to continue to your dashboard</p>

        {/* Email */}
        <label style={styles.label} htmlFor="email">
          Email
        </label>
        <div style={styles.fieldWrap}>
          <span style={styles.fieldIcon}>✉</span>
          <input
            id="email"
            className="login-input"
            style={styles.input}
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && login()}
          />
        </div>

        {/* Password */}
        <label style={styles.label} htmlFor="password">
          Password
        </label>
        <div style={styles.fieldWrap}>
          <span style={styles.fieldIcon}>🔑</span>
          <input
            id="password"
            className="login-input"
            style={styles.input}
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && login()}
          />
        </div>

        <button style={styles.forgot}>Forgot password?</button>

        {/* Login button */}
        <button
          className="login-btn"
          style={getBtnStyle()}
          onClick={login}
          disabled={btnState === "loading" || btnState === "success"}
        >
          {getBtnContent()}
        </button>

        {/* Divider */}
        <div style={styles.dividerWrap}>
          <div style={styles.dividerLine} />
          <span style={styles.dividerText}>or continue with</span>
          <div style={styles.dividerLine} />
        </div>

        {/* Social */}
        <div style={styles.socialRow}>
          <button className="login-social-btn" style={styles.socialBtn}>
            G Google
          </button>
          <button className="login-social-btn" style={styles.socialBtn}>
            ⬡ GitHub
          </button>
        </div>

        <div style={styles.signupRow}>
          Don't have an account?{" "}
          <a href="/signup" style={styles.signupLink}>
            Sign up
          </a>
        </div>
      </div>
    </div>
  );
}