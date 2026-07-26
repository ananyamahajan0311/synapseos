import { useNavigate } from "react-router-dom";
import "../App.css";

function Desktop() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="desktop">

      <div className="sidebar">
        <h2>⚡ SynapseOS</h2>

        <button onClick={logout}>
          Logout
        </button>
      </div>

            <div className="desktop-content">

        <h1>Tell it. It gets done.</h1>

        <p className="subtitle">
          What would you like me to do today?
        </p>

        <div className="prompt-box">

          <textarea
            placeholder={`Type anything...
Example:
Write an apology email to my professor.
Create an attendance sheet.
Schedule tomorrow's AI Lab.`}
          />

          <button>
            Send →
          </button>

        </div>

      </div>

    </div>
  );
}

export default Desktop;