import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Header from "../components/Header";
import ChatMessage from "../components/ChatMessage";
import ChatInput from "../components/ChatInput";

const injectFonts = () => {
  if (document.getElementById("synapse-fonts")) return;

  const link = document.createElement("link");
  link.id = "synapse-fonts";
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

    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulseDot {
      0%, 80%, 100% { opacity: 0.25; transform: scale(0.85); }
      40% { opacity: 1; transform: scale(1); }
    }

    .action-card {
      transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
      animation: fadeInUp 0.35s ease both;
    }

    .action-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 10px 22px rgba(80, 60, 140, 0.16);
      border-color: rgba(120, 100, 170, 0.35);
    }

    .action-card:active {
      transform: scale(0.98);
    }

    .action-card:focus-visible {
      outline: 2px solid #8C7AE6;
      outline-offset: 2px;
    }

    .typing-dot {
      animation: pulseDot 1.2s ease-in-out infinite;
    }

    .try-chip:hover {
      background: #ffffff;
      transform: translateY(-1px);
    }

    .try-chip:active {
      transform: scale(0.97);
    }

    .try-chip:focus-visible {
      outline: 2px solid #8C7AE6;
      outline-offset: 2px;
    }

    @media (prefers-reduced-motion: reduce) {
      .action-card, .cloud-shape, .typing-dot {
        animation: none !important;
      }
    }

    @media (max-width: 560px) {
      .action-grid {
        grid-template-columns: repeat(2, 1fr) !important;
      }
    }
  `;

  document.head.appendChild(styleEl);
};

const styles = {
  page: {
    display: "flex",
    flexDirection: "column",
    height: "100vh",
    background:
      "linear-gradient(180deg, #EFE9F9 0%, #E3DAF4 45%, #D8CCEF 100%)",
    fontFamily: "'Nunito', sans-serif",
    position: "relative",
    overflow: "hidden",
  },

  cloud: {
    position: "absolute",
    background: "#ffffff99",
    borderRadius: "50%",
    animation: "float 7s ease-in-out infinite",
    pointerEvents: "none",
    zIndex: 0,
  },

  scrollArea: {
    flex: 1,
    overflowY: "auto",
    padding: "24px",
    position: "relative",
    zIndex: 1,
  },

  inner: {
    margin: "0 auto",
    maxWidth: "900px",
  },

  capabilityTitle: {
    textAlign: "center",
    fontFamily: "'Baloo 2', sans-serif",
    fontSize: "21px",
    fontWeight: 800,
    color: "#4C3F72",
    margin: "20px 0 14px",
  },

  capabilitySubtitle: {
    textAlign: "center",
    fontSize: "13px",
    color: "#756B91",
    marginBottom: "18px",
  },

  category: {
    marginBottom: "20px",
  },

  categoryTitle: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    fontFamily: "'Baloo 2', sans-serif",
    fontSize: "16px",
    fontWeight: 800,
    color: "#5B4A82",
    marginBottom: "10px",
  },

  categoryDot: {
    width: "8px",
    height: "8px",
    borderRadius: "50%",
    flexShrink: 0,
  },

  actionGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)",
    gap: "10px",
  },

  actionCard: {
    border: "1px solid rgba(120, 100, 170, 0.18)",
    borderRadius: "14px",
    background: "rgba(255, 255, 255, 0.8)",
    padding: "14px",
    cursor: "pointer",
    textAlign: "left",
    boxShadow: "0 3px 10px rgba(80, 60, 140, 0.06)",
  },

  actionIconBadge: {
    width: "32px",
    height: "32px",
    borderRadius: "10px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "16px",
    marginBottom: "8px",
  },

  actionName: {
    fontWeight: 800,
    color: "#4C3F72",
    fontSize: "13px",
  },

  actionDescription: {
    fontSize: "10px",
    color: "#817797",
    marginTop: "2px",
  },

  tryBox: {
    background: "rgba(255,255,255,0.55)",
    border: "1px solid rgba(120,100,170,0.15)",
    borderRadius: "16px",
    padding: "16px 18px",
    margin: "24px 0",
  },

  tryTitle: {
    fontFamily: "'Baloo 2', sans-serif",
    fontWeight: 800,
    color: "#5B4A82",
    fontSize: "15px",
    marginBottom: "10px",
  },

  tryChips: {
    display: "flex",
    flexWrap: "wrap",
    gap: "8px",
  },

  tryChip: {
    fontSize: "12px",
    color: "#5B4A82",
    background: "#ffffffb0",
    border: "1px solid rgba(120,100,170,0.22)",
    borderRadius: "999px",
    padding: "6px 12px",
    cursor: "pointer",
    fontWeight: 700,
    transition: "background 0.15s ease, transform 0.15s ease",
  },

  inputOuter: {
    margin: "0 auto",
    width: "100%",
    maxWidth: "900px",
    padding: "0 24px 24px",
    position: "relative",
    zIndex: 1,
  },

  typingRow: {
    display: "flex",
    gap: "5px",
    alignItems: "center",
    padding: "10px 14px",
    width: "fit-content",
    background: "rgba(255,255,255,0.7)",
    borderRadius: "14px",
    margin: "6px 0 16px",
  },

  typingDot: {
    width: "6px",
    height: "6px",
    borderRadius: "50%",
    background: "#8C7AE6",
  },
};

const clouds = [
  { width: 70, height: 40, top: "8%", left: "6%", delay: "0s" },
  { width: 50, height: 30, top: "14%", right: "9%", delay: "1.5s" },
  { width: 60, height: 34, bottom: "14%", left: "4%", delay: "0.8s" },
  { width: 42, height: 24, bottom: "22%", right: "6%", delay: "2.2s" },
];

const tryPrompts = [
  "Show me my latest emails.",
  "Create a meeting tomorrow at 10 AM.",
  "Create a Google Doc about artificial intelligence.",
  "Calculate 25% of 840.",
  "Create a spreadsheet for my project tasks.",
  "Open Google.",
];

const actions = [
  {
    category: "📧 Email",
    accent: "#E58A8A",
    items: [
      {
        icon: "✉️",
        name: "Send Email",
        description: "Send an email",
        prompt: "Send an email to someone with a subject and message",
      },
      {
        icon: "🔍",
        name: "Search Email",
        description: "Find specific emails",
        prompt: "Search my emails for",
      },
      {
        icon: "📥",
        name: "Read Emails",
        description: "View latest emails",
        prompt: "Show me my latest emails",
      },
    ],
  },

  {
    category: "📅 Calendar",
    accent: "#7AA6D9",
    items: [
      {
        icon: "➕",
        name: "Create Event",
        description: "Schedule a meeting",
        prompt: "Create a calendar event",
      },
      {
        icon: "📋",
        name: "View Events",
        description: "See upcoming events",
        prompt: "Show me my upcoming calendar events",
      },
      {
        icon: "🗑️",
        name: "Delete Event",
        description: "Remove an event",
        prompt: "Delete a calendar event",
      },
    ],
  },

  {
    category: "📄 Google Docs",
    accent: "#7AC0A6",
    items: [
      {
        icon: "➕",
        name: "Create Document",
        description: "Create a Google Doc",
        prompt: "Create a Google Doc about",
      },
      {
        icon: "📋",
        name: "List Documents",
        description: "View your documents",
        prompt: "Show me my Google Documents",
      },
    ],
  },

  {
    category: "📊 Google Sheets",
    accent: "#D9B15A",
    items: [
      {
        icon: "➕",
        name: "Create Sheet",
        description: "Create a spreadsheet",
        prompt: "Create a Google Sheet for",
      },
    ],
  },

  {
    category: "🛠️ Other Tools",
    accent: "#9B8AD9",
    items: [
      {
        icon: "🧮",
        name: "Calculate",
        description: "Perform calculations",
        prompt: "Calculate",
      },
      {
        icon: "🌐",
        name: "Open Website",
        description: "Open a website",
        prompt: "Open Google",
      },
      {
        icon: "🕐",
        name: "Date & Time",
        description: "Get current date and time",
        prompt: "What is the current date and time?",
      },
    ],
  },
];

function Desktop() {
  const navigate = useNavigate();
  injectFonts();

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "👋 Hi! I'm SynapseOS.\nHow can I help you today?",
    },
  ]);
  const [isThinking, setIsThinking] = useState(false);

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  const handleSend = async (prompt) => {
    if (!prompt || !prompt.trim()) return;

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: prompt,
      },
    ]);

    setIsThinking(true);

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

      console.log("Backend Response:", data);

      let botMessage = "";

      // Show tools used
      if (data.plan && Array.isArray(data.plan)) {
        data.plan.forEach((step, index) => {
          if (step.tool !== "chat") {
            botMessage += `🔧 Step ${index + 1}: ${step.tool}\n`;
          }
        });

        if (botMessage !== "") {
          botMessage += "\n";
        }
      }

      // Show results
      if (data.results && Array.isArray(data.results)) {
        data.results.forEach((result, index) => {
          botMessage += `✅ Result ${index + 1}\n`;
          botMessage += `${result.message}\n\n`;
        });
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
    } finally {
      setIsThinking(false);
    }
  };

  const handleCardKeyDown = (event, prompt) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      handleSend(prompt);
    }
  };

  return (
    <div style={styles.page}>

      {/* Decorative clouds */}
      {clouds.map((cloud, index) => (
        <div
          key={index}
          className="cloud-shape"
          style={{
            ...styles.cloud,
            width: cloud.width,
            height: cloud.height,
            top: cloud.top,
            left: cloud.left,
            right: cloud.right,
            bottom: cloud.bottom,
            animationDelay: cloud.delay,
          }}
        />
      ))}

      <Header logout={logout} />

      <div style={styles.scrollArea}>
        <div style={styles.inner}>

          {/* Chat */}
          {messages.map((msg, index) => (
            <ChatMessage
              key={index}
              sender={msg.sender}
              text={msg.text}
            />
          ))}

          {isThinking && (
            <div style={styles.typingRow} aria-live="polite" aria-label="SynapseOS is thinking">
              <span className="typing-dot" style={{ ...styles.typingDot, animationDelay: "0s" }} />
              <span className="typing-dot" style={{ ...styles.typingDot, animationDelay: "0.2s" }} />
              <span className="typing-dot" style={{ ...styles.typingDot, animationDelay: "0.4s" }} />
            </div>
          )}

          {/* Capabilities */}
          <div style={styles.capabilityTitle}>
            ✨ What can SynapseOS do?
          </div>

          <div style={styles.capabilitySubtitle}>
            Click an action to try it, or simply describe what you want
            in natural language.
          </div>

          {actions.map((group) => (
            <div key={group.category} style={styles.category}>

              <div style={styles.categoryTitle}>
                <span
                  style={{ ...styles.categoryDot, background: group.accent }}
                />
                {group.category}
              </div>

              <div className="action-grid" style={styles.actionGrid}>
                {group.items.map((item, itemIndex) => (
                  <div
                    key={item.name}
                    className="action-card"
                    style={{
                      ...styles.actionCard,
                      animationDelay: `${itemIndex * 0.05}s`,
                    }}
                    role="button"
                    tabIndex={0}
                    onClick={() => handleSend(item.prompt)}
                    onKeyDown={(event) => handleCardKeyDown(event, item.prompt)}
                  >
                    <div
                      style={{
                        ...styles.actionIconBadge,
                        background: `${group.accent}26`,
                      }}
                    >
                      {item.icon}
                    </div>

                    <div style={styles.actionName}>
                      {item.name}
                    </div>

                    <div style={styles.actionDescription}>
                      {item.description}
                    </div>
                  </div>
                ))}
              </div>

            </div>
          ))}

          {/* Example prompts */}
          <div style={styles.tryBox}>
            <div style={styles.tryTitle}>
              💡 Try asking SynapseOS
            </div>

            <div style={styles.tryChips}>
              {tryPrompts.map((prompt) => (
                <button
                  key={prompt}
                  type="button"
                  className="try-chip"
                  style={styles.tryChip}
                  onClick={() => handleSend(prompt)}
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>

        </div>
      </div>

      {/* Chat input */}
      <div style={styles.inputOuter}>
        <ChatInput onSend={handleSend} />
      </div>

    </div>
  );
}

export default Desktop;