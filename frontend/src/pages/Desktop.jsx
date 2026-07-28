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
      text: "👋 Hi! I'm SynapseOS.\nHow can I help you today?",
    },
  ]);

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  const handleSend = async (prompt) => {
    // Show user's message
    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: prompt,
      },
    ]);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to connect to backend");
      }

      const data = await response.json();

      let botMessage = "";

      // Show selected tool if available
      if (data.plan && data.plan.tool && data.plan.tool !== "chat") {
        botMessage += `🔧 Tool: ${data.plan.tool}\n\n`;
      }

      // Show result
      if (data.result && data.result.message) {
        botMessage += data.result.message;
      } else if (data.result) {
        botMessage += JSON.stringify(data.result, null, 2);
      } else {
        botMessage += "No response received.";
      }

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: botMessage,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "❌ Unable to connect to SynapseOS backend.",
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

      <div className="mx-auto w-full max-w-4xl pb-6">
        <ChatInput onSend={handleSend} />
      </div>
    </div>
  );
}

export default Desktop;