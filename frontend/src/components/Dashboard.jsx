import { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import "../App.css";

function Dashboard() {

  const navigate = useNavigate();

  const [prompt, setPrompt] = useState("");

  const [email, setEmail] = useState("");

  const [toEmail, setToEmail] = useState("");

  const [history, setHistory] = useState([]);

  useEffect(() => {

  const token = localStorage.getItem("token");

  if (!token) {

    navigate("/");

    return;
  }

  fetch("http://127.0.0.1:8000/email-history")
    .then((res) => res.json())
    .then((data) => setHistory(data));

}, []);

  const logout = () => {

    localStorage.removeItem("token");

    navigate("/");

  };

  const generateEmail = async () => {

    const response = await fetch(
      "http://127.0.0.1:8000/generate-email",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          prompt,
        }),
      }
    );

    const data = await response.json();

    setEmail(data.email);
  };

  const sendEmail = async () => {

    await fetch(
      "http://127.0.0.1:8000/send-email",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          to_email: toEmail,
          subject: "AI Generated Email",
          message: email,
        }),
      }
    );

    alert("Email sent successfully");
  };

  return (

    <div className="dashboard">

      <div className="sidebar">

        <h2>SynapseOS</h2>

        <button onClick={logout}>
          Logout
        </button>

      </div>

      <div className="dashboard-content">

        <h1>SynapseOS Dashboard</h1>

        <textarea
          placeholder="Enter prompt..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />

        <button onClick={generateEmail}>
          Generate Email
        </button>

        <div className="email-box">

          <h2>Generated Email</h2>

          <textarea
  value={email}
  readOnly
  rows="10"
  style={{
    width: "100%",
    marginTop: "20px"
  }}
/>

          <input
            placeholder="Recipient Email"
            value={toEmail}
            onChange={(e) => setToEmail(e.target.value)}
          />

          <button onClick={sendEmail}>
            Send Email
          </button>
        </div>

        <div className="history-box">

          <h2>Email History</h2>

          {history.map((item) => (

            <div key={item.id}>

              <p><b>To:</b> {item.recipient}</p>

              <p><b>Subject:</b> {item.subject}</p>

              <hr />

            </div>

          ))}

        </div>

      </div>

    </div>
  );
}

export default Dashboard;