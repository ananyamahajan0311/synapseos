import { useState } from "react";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  const generateEmail = async () => {
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/generate-email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: prompt,
        }),
      });

      const data = await response.json();

      setEmail(data.email);
    } catch (error) {
      setEmail("Error generating email");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1>SynapseOS</h1>

      <textarea
        placeholder="Enter your email prompt..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      <button onClick={generateEmail}>
        Generate Email
      </button>

      {loading && <p>Generating...</p>}

      {email && (
        <div className="output">
          <h2>Generated Email</h2>
          <p>{email}</p>
        </div>
      )}
    </div>
  );
}

export default App;