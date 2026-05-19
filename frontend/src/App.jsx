import { useState } from "react";
import "./App.css";

function App() {

  const [prompt, setPrompt] = useState("");
  const [email, setEmail] = useState("");
  const [recipient, setRecipient] = useState("");
  const [loading, setLoading] = useState(false);
  const [sendMessage, setSendMessage] = useState("");

  const generateEmail = async () => {

    setLoading(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/generate-email",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            prompt: prompt,
          }),
        }
      );

      const data = await response.json();

      setEmail(data.email);

    } catch (error) {

      setEmail("Error generating email");

    }

    setLoading(false);
  };

  const sendEmail = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/send-email",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            to_email: recipient,
            subject: "AI Generated Email from SynapseOS",
            message: email,
          }),
        }
      );

      const data = await response.json();

      setSendMessage(data.message);

    } catch (error) {

  setEmail(
`Dear Sir/Madam,

I sincerely apologize for submitting my assignment late. Due to unforeseen circumstances, I was unable to complete it on time.

I take full responsibility and assure you this will not happen again.

Thank you for your understanding.

Regards,
Student`
  );

}
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

          <input
            type="email"
            placeholder="Enter recipient email"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
          />

          <button onClick={sendEmail}>
            Send Email
          </button>

          {sendMessage && <p>{sendMessage}</p>}

        </div>
      )}

    </div>
  );
}

export default App;