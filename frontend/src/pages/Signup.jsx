import { useState } from "react";

const styles = `
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&family=Syne:wght@600&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  .su-root {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0e0e11;
    font-family: 'DM Sans', sans-serif;
    padding: 2rem 1rem;
  }

  .su-bg {
    position: fixed;
    inset: 0;
    pointer-events: none;
    overflow: hidden;
    z-index: 0;
  }
  .su-bg::before {
    content: '';
    position: absolute;
    width: 600px; height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(127,119,221,0.18) 0%, transparent 70%);
    top: -200px; left: -100px;
  }
  .su-bg::after {
    content: '';
    position: absolute;
    width: 400px; height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(93,202,165,0.12) 0%, transparent 70%);
    bottom: -100px; right: -50px;
  }

  .su-card {
    position: relative;
    z-index: 1;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    width: 100%;
    max-width: 420px;
    backdrop-filter: blur(12px);
  }

  .su-header {
    text-align: center;
    margin-bottom: 2rem;
  }
  .su-icon-ring {
    width: 56px; height: 56px;
    border-radius: 50%;
    border: 1px solid rgba(127,119,221,0.4);
    background: rgba(127,119,221,0.12);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 1.25rem;
    font-size: 22px;
  }
  .su-title {
    font-family: 'Syne', sans-serif;
    font-size: 24px;
    font-weight: 600;
    color: #fff;
    margin-bottom: 6px;
  }
  .su-sub {
    font-size: 14px;
    color: rgba(255,255,255,0.45);
  }

  .su-field { margin-bottom: 1rem; }
  .su-label {
    display: block;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.4);
    margin-bottom: 8px;
  }
  .su-input-wrap {
    position: relative;
    display: flex;
    align-items: center;
  }
  .su-input-icon {
    position: absolute;
    left: 14px;
    font-size: 15px;
    color: rgba(255,255,255,0.3);
    pointer-events: none;
  }
  .su-input {
    width: 100%;
    height: 46px;
    padding: 0 14px 0 42px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 10px;
    font-size: 15px;
    font-family: 'DM Sans', sans-serif;
    color: #fff;
    outline: none;
    transition: border-color 0.2s, background 0.2s;
  }
  .su-input::placeholder { color: rgba(255,255,255,0.2); }
  .su-input:focus {
    border-color: rgba(127,119,221,0.6);
    background: rgba(127,119,221,0.08);
  }
  .su-pw-toggle {
    position: absolute;
    right: 14px;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 15px;
    color: rgba(255,255,255,0.3);
    padding: 0;
    transition: color 0.15s;
  }
  .su-pw-toggle:hover { color: rgba(255,255,255,0.65); }

  .su-btn {
    width: 100%;
    height: 48px;
    margin-top: 1.5rem;
    background: #7F77DD;
    border: none;
    border-radius: 10px;
    color: #fff;
    font-size: 15px;
    font-weight: 500;
    font-family: 'DM Sans', sans-serif;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: opacity 0.15s, transform 0.1s;
  }
  .su-btn:hover:not(:disabled) { opacity: 0.85; }
  .su-btn:active:not(:disabled) { transform: scale(0.98); }
  .su-btn:disabled { opacity: 0.45; cursor: not-allowed; }

  .su-spinner {
    width: 16px; height: 16px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: su-spin 0.7s linear infinite;
  }
  @keyframes su-spin { to { transform: rotate(360deg); } }

  .su-divider {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.5rem 0 0;
    font-size: 13px;
    color: rgba(255,255,255,0.2);
  }
  .su-divider::before, .su-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.08);
  }
  .su-signin {
    text-align: center;
    font-size: 14px;
    color: rgba(255,255,255,0.35);
    margin-top: 1rem;
  }
  .su-signin a {
    color: #9E98E8;
    text-decoration: none;
    font-weight: 500;
  }
  .su-signin a:hover { text-decoration: underline; }

  .su-toast {
    position: fixed;
    bottom: 28px;
    left: 50%;
    transform: translateX(-50%) translateY(12px);
    background: rgba(30,30,36,0.95);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    padding: 12px 20px;
    font-size: 14px;
    font-family: 'DM Sans', sans-serif;
    color: #fff;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s, transform 0.2s;
    z-index: 9999;
    white-space: nowrap;
  }
  .su-toast.visible {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
`;

export default function Signup() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPw, setShowPw] = useState(false);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState({ msg: "", visible: false });

  const showToast = (msg) => {
    setToast({ msg, visible: true });
    setTimeout(() => setToast({ msg: "", visible: false }), 3000);
  };

  const signup = async () => {
    if (!username.trim() || !email.trim() || !password) {
      showToast("Please fill in all fields.");
      return;
    }
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });
      const data = await response.json();
      showToast(data.message || "Account created!");
    } catch {
      showToast("Could not reach the server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <style>{styles}</style>
      <div className="su-root">
        <div className="su-bg" />
        <div className="su-card">
          <div className="su-header">
            <div className="su-icon-ring">✦</div>
            <p style={{ fontFamily: "'Syne', sans-serif", fontSize: "13px", letterSpacing: "3px", textTransform: "uppercase", color: "rgba(127,119,221,0.8)", marginBottom: "8px" }}>SynapseOS</p>
            <h1 className="su-title">Create your account</h1>
            <p className="su-sub">Join thousands of users today</p>
            <p style={{ fontSize: "11px", color: "rgba(255,255,255,0.2)", marginTop: "6px", letterSpacing: "1px" }}>by Ananya Mahajan</p>
          </div>

          <div className="su-field">
            <label className="su-label" htmlFor="username">Username</label>
            <div className="su-input-wrap">
              <span className="su-input-icon">@</span>
              <input
                id="username"
                className="su-input"
                type="text"
                placeholder="yourname"
                autoComplete="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
          </div>

          <div className="su-field">
            <label className="su-label" htmlFor="email">Email</label>
            <div className="su-input-wrap">
              <span className="su-input-icon">✉</span>
              <input
                id="email"
                className="su-input"
                type="email"
                placeholder="you@example.com"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          <div className="su-field">
            <label className="su-label" htmlFor="password">Password</label>
            <div className="su-input-wrap">
              <span className="su-input-icon">🔒</span>
              <input
                id="password"
                className="su-input"
                type={showPw ? "text" : "password"}
                placeholder="Min. 8 characters"
                autoComplete="new-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{ paddingRight: "42px" }}
              />
              <button
                className="su-pw-toggle"
                type="button"
                aria-label="Toggle password visibility"
                onClick={() => setShowPw((v) => !v)}
              >
                {showPw ? "🙈" : "👁"}
              </button>
            </div>
          </div>

          <button className="su-btn" onClick={signup} disabled={loading}>
            {loading ? (
              <><div className="su-spinner" /> Creating account…</>
            ) : (
              <>Create account →</>
            )}
          </button>

          <div className="su-divider">or</div>
          <div className="su-signin">
            Already have an account? <a href="#">Sign in</a>
          </div>
        </div>
      </div>

      <div className={`su-toast${toast.visible ? " visible" : ""}`}>
        {toast.msg}
      </div>
    </>
  );
}