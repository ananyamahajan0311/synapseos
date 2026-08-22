import { useState } from "react";

const styles = {
  wrap: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    background: "#FDFCFB",
    border: "1.5px solid #ECE7F7",
    borderRadius: "28px",
    padding: "6px 6px 6px 20px",
    boxShadow: "0 14px 30px -18px rgba(90,70,140,0.4)",
  },
  input: {
    flex: 1,
    border: "none",
    outline: "none",
    background: "transparent",
    fontFamily: "'Nunito', sans-serif",
    fontSize: "14.5px",
    fontWeight: 700,
    color: "#4A3F6B",
    height: "36px",
  },
  sendBtn: {
    width: "42px",
    height: "42px",
    minWidth: "42px",
    borderRadius: "50%",
    border: "none",
    background: "linear-gradient(135deg, #9C8FE6, #7C6DD8)",
    color: "#fff",
    fontSize: "16px",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    transition: "transform 0.12s, opacity 0.12s",
    boxShadow: "0 8px 18px -8px rgba(124,109,216,0.7)",
  },
};

export default function ChatInput({ onSend }) {
  const [value, setValue] = useState("");

  const submit = () => {
    const trimmed = value.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setValue("");
  };

  return (
    <div style={styles.wrap}>
      <input
        style={styles.input}
        className="chat-input-field"
        type="text"
        placeholder="Ask SynapseOS anything..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && submit()}
      />
      <button
        className="chat-send-btn"
        style={styles.sendBtn}
        onClick={submit}
        aria-label="Send message"
      >
        ➤
      </button>

      <style>{`
        .chat-input-field::placeholder {
          color: #C3BBDB;
          font-weight: 700;
        }
        .chat-send-btn:hover {
          transform: translateY(-1px);
          opacity: 0.95;
        }
        .chat-send-btn:active {
          transform: scale(0.94) !important;
        }
      `}</style>
    </div>
  );
}