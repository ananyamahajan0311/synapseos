import { useState } from "react";
import { useNavigate } from "react-router-dom";

const styles = {
  wrap: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background:
      "linear-gradient(180deg, #EFE9F9 0%, #E3DAF4 45%, #D8CCEF 100%)",
    fontFamily: "'Nunito', sans-serif",
    padding: "2.5rem 1rem",
    position: "relative",
    overflow: "hidden",
  },
  cloud: {
    position: "absolute",
    background: "#ffffffaa",
    borderRadius: "50%",
    filter: "blur(0.5px)",
    animation: "float 6s ease-in-out infinite",
  },
  potWrap: {
    position: "absolute",
    bottom: "6%",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  cardOuter: {
    width: "100%",
    maxWidth: "380px",
    position: "relative",
    zIndex: 2,
  },
  character: {
    position: "relative",
    zIndex: 3,
    display: "flex",
    justifyContent: "center",
    marginBottom: "-38px",
  },
  card: {
    width: "100%",
    background: "#FDFCFB",
    borderRadius: "32px",
    padding: "56px 2rem 2rem",
    boxShadow: "0 30px 60px -20px rgba(90, 70, 140, 0.35)",
    position: "relative",
    boxSizing: "border-box",
  },
  headWrap: {
    textAlign: "center",
    marginBottom: "1.75rem",
  },
  title: {
    fontFamily: "'Baloo 2', sans-serif",
    fontSize: "26px",
    fontWeight: 700,
    color: "#4A3F6B",
    margin: "0 0 4px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "8px",
  },
  sub: {
    fontSize: "13.5px",
    color: "#9B92B3",
    margin: 0,
    fontWeight: 600,
  },
  fieldWrap: {
    position: "relative",
    marginBottom: "1rem",
  },
  fieldIconWrap: {
    position: "absolute",
    left: "6px",
    top: "6px",
    width: "32px",
    height: "32px",
    borderRadius: "50%",
    background: "linear-gradient(135deg, #A79AE8, #8B7BDC)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "#fff",
    fontSize: "14px",
    pointerEvents: "none",
  },
  input: {
    width: "100%",
    height: "44px",
    padding: "0 40px 0 48px",
    borderRadius: "22px",
    border: "1.5px solid #ECE7F7",
    background: "#F7F4FC",
    fontSize: "14px",
    fontFamily: "'Nunito', sans-serif",
    fontWeight: 600,
    color: "#4A3F6B",
    outline: "none",
    boxSizing: "border-box",
    transition: "border-color 0.15s, box-shadow 0.15s",
  },
  eyeToggle: {
    position: "absolute",
    right: "14px",
    top: "50%",
    transform: "translateY(-50%)",
    background: "none",
    border: "none",
    color: "#B4ABCB",
    cursor: "pointer",
    fontSize: "16px",
    padding: 0,
    display: "flex",
  },
  forgot: {
    display: "block",
    textAlign: "right",
    fontSize: "12px",
    color: "#8B7BDC",
    textDecoration: "none",
    marginBottom: "1.4rem",
    cursor: "pointer",
    background: "none",
    border: "none",
    fontWeight: 700,
    padding: 0,
  },
  btn: {
    width: "100%",
    height: "48px",
    borderRadius: "24px",
    border: "none",
    background: "linear-gradient(135deg, #9C8FE6, #7C6DD8)",
    color: "#fff",
    fontFamily: "'Baloo 2', sans-serif",
    fontSize: "16px",
    fontWeight: 700,
    letterSpacing: "0.02em",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "8px",
    transition: "transform 0.12s, opacity 0.12s",
    boxShadow: "0 10px 24px -8px rgba(124, 109, 216, 0.7)",
  },
  dividerWrap: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    margin: "1.5rem 0 1.25rem",
  },
  dividerLine: {
    flex: 1,
    height: "1px",
    background: "#ECE7F7",
  },
  dividerText: {
    fontSize: "12px",
    color: "#B4ABCB",
    whiteSpace: "nowrap",
    fontWeight: 700,
  },
  socialRow: {
    display: "flex",
    gap: "12px",
    justifyContent: "center",
  },
  socialBtn: {
    width: "44px",
    height: "44px",
    borderRadius: "50%",
    border: "1.5px solid #ECE7F7",
    background: "#fff",
    fontSize: "18px",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    transition: "transform 0.12s, border-color 0.12s",
  },
  signupRow: {
    textAlign: "center",
    marginTop: "1.5rem",
    fontSize: "13px",
    color: "#9B92B3",
    fontWeight: 600,
  },
  signupLink: {
    color: "#8B7BDC",
    textDecoration: "none",
    fontWeight: 800,
  },
};

const injectFonts = () => {
  if (document.getElementById("login-fonts")) return;
  const link = document.createElement("link");
  link.id = "login-fonts";
  link.rel = "stylesheet";
  link.href =
    "https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;600;700;800&display=swap";
  document.head.appendChild(link);

  const styleEl = document.createElement("style");
  styleEl.textContent = `
    @keyframes float {
      0%, 100% { transform: translateY(0px); }
      50% { transform: translateY(-10px); }
    }
    @keyframes bob {
      0%, 100% { transform: translateY(0px) rotate(-1deg); }
      50% { transform: translateY(-6px) rotate(1deg); }
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    .login-input:focus {
      border-color: #8B7BDC !important;
      box-shadow: 0 0 0 3px #8B7BDC22 !important;
      background: #fff !important;
    }
    .login-input::placeholder {
      color: #C3BBDB;
      font-weight: 600;
    }
    .login-social-btn:hover {
      transform: translateY(-2px);
      border-color: #C9BFEA !important;
    }
    .login-btn:hover {
      transform: translateY(-2px);
      opacity: 0.95;
    }
    .login-btn:active {
      transform: scale(0.98) !important;
    }
    .login-character {
      animation: bob 4.5s ease-in-out infinite;
    }
  `;
  document.head.appendChild(styleEl);
};

function PlantPot({ side }) {
  return (
    <div style={{ ...styles.potWrap, [side]: "4%" }}>
      <svg width="90" height="110" viewBox="0 0 90 110" fill="none">
        <ellipse cx="45" cy="98" rx="26" ry="8" fill="#00000014" />
        <path d="M20 55 L28 100 H62 L70 55 Z" fill="#D8A97C" />
        <path d="M20 55 L70 55 L66 68 H24 Z" fill="#C79066" />
        <path
          d="M45 55 C 20 45, 15 15, 40 5 C 38 25, 42 40, 45 55 Z"
          fill="#6FAE7C"
        />
        <path
          d="M45 55 C 70 40, 78 12, 55 2 C 55 22, 50 40, 45 55 Z"
          fill="#5C9A69"
        />
        <path
          d="M45 55 C 45 25, 48 8, 45 0 C 42 8, 45 25, 45 55 Z"
          fill="#82BB8E"
        />
      </svg>
    </div>
  );
}

function Character() {
  return (
    <div style={styles.character}>
      <svg
        className="login-character"
        width="170"
        height="150"
        viewBox="0 0 170 150"
        fill="none"
      >
        {/* hood/hair back */}
        <ellipse cx="85" cy="78" rx="58" ry="52" fill="#6E5FBF" />
        {/* face */}
        <ellipse cx="85" cy="66" rx="40" ry="38" fill="#F7C9A0" />
        {/* hair front */}
        <path
          d="M45 60 C 40 25, 130 25, 125 60 C 118 45, 100 38, 85 40 C 70 38, 52 45, 45 60 Z"
          fill="#4A3A2A"
        />
        <circle cx="60" cy="35" r="9" fill="#4A3A2A" />
        <circle cx="110" cy="35" r="9" fill="#4A3A2A" />
        {/* blush */}
        <ellipse cx="62" cy="74" rx="7" ry="5" fill="#F7A98C" opacity="0.7" />
        <ellipse cx="108" cy="74" rx="7" ry="5" fill="#F7A98C" opacity="0.7" />
        {/* eyes - one winking */}
        <path
          d="M55 62 Q 62 56 69 62"
          stroke="#3A2E22"
          strokeWidth="3.5"
          strokeLinecap="round"
          fill="none"
        />
        <circle cx="107" cy="63" r="4.5" fill="#3A2E22" />
        {/* smile */}
        <path
          d="M75 84 Q 85 92 95 84"
          stroke="#3A2E22"
          strokeWidth="3.5"
          strokeLinecap="round"
          fill="none"
        />
        {/* hoodie shoulders + arms resting on card edge */}
        <path
          d="M20 150 C 20 100, 45 88, 85 88 C 125 88, 150 100, 150 150 Z"
          fill="#8B7BDC"
        />
        <ellipse cx="42" cy="118" rx="16" ry="13" fill="#8B7BDC" />
        <ellipse cx="128" cy="118" rx="16" ry="13" fill="#8B7BDC" />
        <ellipse cx="38" cy="128" rx="11" ry="9" fill="#F7C9A0" />
        <ellipse cx="132" cy="128" rx="11" ry="9" fill="#F7C9A0" />
      </svg>
    </div>
  );
}

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [btnState, setBtnState] = useState("idle"); // idle | loading | success | error
  const navigate = useNavigate();

  injectFonts();

  const getBtnStyle = () => {
    const base = { ...styles.btn };
    if (btnState === "error")
      base.background = "linear-gradient(135deg, #E88A7D, #D96B5A)";
    if (btnState === "success")
      base.background = "linear-gradient(135deg, #6FC79A, #4FAE7E)";
    return base;
  };

  const getBtnContent = () => {
    if (btnState === "loading")
      return (
        <>
          <span style={{ display: "inline-flex", animation: "spin 0.8s linear infinite" }}>
            ⏳
          </span>
          Signing in…
        </>
      );
    if (btnState === "success") return <>✓ Success!</>;
    if (btnState === "error") return <>! Check your details</>;
    return <>Login</>;
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
      console.log("LOGIN RESPONSE:", data);
      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        setBtnState("success");
        setTimeout(() => navigate("/desktop"), 800);
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
      {/* decorative clouds */}
      <div style={{ ...styles.cloud, width: 70, height: 40, top: "12%", left: "8%" }} />
      <div style={{ ...styles.cloud, width: 50, height: 30, top: "20%", right: "10%", animationDelay: "1.5s" }} />
      <div style={{ ...styles.cloud, width: 90, height: 50, bottom: "18%", right: "6%", animationDelay: "0.8s" }} />

      <PlantPot side="left" />
      <PlantPot side="right" />

      <div style={styles.cardOuter}>
        <Character />
        <div style={styles.card}>
          <div style={styles.headWrap}>
            <h1 style={styles.title}>✨ Welcome Back ✨</h1>
            <p style={styles.sub}>Login to continue your journey</p>
          </div>

          {/* Email */}
          <div style={styles.fieldWrap}>
            <span style={styles.fieldIconWrap}>👤</span>
            <input
              id="email"
              className="login-input"
              style={styles.input}
              type="email"
              placeholder="Email or Username"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && login()}
            />
          </div>

          {/* Password */}
          <div style={styles.fieldWrap}>
            <span style={styles.fieldIconWrap}>🔒</span>
            <input
              id="password"
              className="login-input"
              style={styles.input}
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && login()}
            />
            <button
              type="button"
              style={styles.eyeToggle}
              onClick={() => setShowPassword((s) => !s)}
              aria-label={showPassword ? "Hide password" : "Show password"}
            >
              {showPassword ? "🙈" : "👁"}
            </button>
          </div>

          <button style={styles.forgot} type="button">
            Forgot Password?
          </button>

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
            <button className="login-social-btn" style={styles.socialBtn} aria-label="Continue with Google">
              G
            </button>
            <button className="login-social-btn" style={styles.socialBtn} aria-label="Continue with Apple">
              
            </button>
            <button className="login-social-btn" style={styles.socialBtn} aria-label="Continue with Facebook">
              f
            </button>
          </div>

          <div style={styles.signupRow}>
            Don't have an account?{" "}
            <a href="/signup" style={styles.signupLink}>
              Sign Up
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}