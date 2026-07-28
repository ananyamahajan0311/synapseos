import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Header from "../components/Header";
import ChatMessage from "../components/ChatMessage";
import ChatInput from "../components/ChatInput";

function Desktop() {
  const navigate = useNavigate();

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hi! I'm SynapseOS. What would you like me to do today?",
    },
  ]);

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  const handleSend = async (prompt) => {
    const planText =
  data.plan.tool === "chat"
    ? "No tool selected"
    : `Selected Tool: ${data.plan.tool}`;

const botResponse = `${planText}

${data.result.message}`;

setMessages((prev) => [
  ...prev,
  {
    sender: "bot",
    text: botResponse,
  },
]);
    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: prompt,
        }),
      });

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text:
  data.result.message || JSON.stringify(data.result),
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "❌ Unable to connect to backend.",
        },
      ]);
    }
  };

  return (
    <div className="flex h-screen flex-col bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 text-white">
      <Header logout={logout} />

      <div className="flex-1 overflow-y-auto px-6 py-6">
        <div className="mx-auto max-w-4xl">
          {messages.map((msg, index) => (
            <ChatMessage
              key={index}
              sender={msg.sender}
              text={msg.text}
            />
          ))}
        </div>
      </div>

      <div className="mx-auto w-full max-w-4xl">
        <ChatInput onSend={handleSend} />
      </div>
    </div>
  );
}

export default Desktop;