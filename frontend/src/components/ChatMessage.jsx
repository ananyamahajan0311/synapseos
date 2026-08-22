const styles = {
  row: {
    display: "flex",
    gap: "10px",
    marginBottom: "18px",
    alignItems: "flex-start",
  },
  avatar: {
    width: "34px",
    height: "34px",
    minWidth: "34px",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "16px",
    marginTop: "2px",
  },
  botAvatar: {
    background: "linear-gradient(135deg, #A79AE8, #8B7BDC)",
    color: "#fff",
    boxShadow: "0 6px 14px -6px rgba(124,109,216,0.5)",
  },
  userAvatar: {
    background: "#EDE7FA",
    color: "#8B7BDC",
  },
  bubbleBot: {
    background: "#FDFCFB",
    color: "#4A3F6B",
    border: "1.5px solid #ECE7F7",
    borderRadius: "22px 22px 22px 6px",
    padding: "12px 18px",
    maxWidth: "72%",
    fontSize: "14.5px",
    lineHeight: 1.55,
    fontWeight: 600,
    whiteSpace: "pre-wrap",
    boxShadow: "0 8px 20px -14px rgba(90,70,140,0.3)",
  },
  bubbleUser: {
    background: "linear-gradient(135deg, #9C8FE6, #7C6DD8)",
    color: "#fff",
    borderRadius: "22px 22px 6px 22px",
    padding: "12px 18px",
    maxWidth: "72%",
    fontSize: "14.5px",
    lineHeight: 1.55,
    fontWeight: 600,
    whiteSpace: "pre-wrap",
    boxShadow: "0 10px 22px -10px rgba(124,109,216,0.55)",
  },
};

export default function ChatMessage({ sender, text }) {
  const isUser = sender === "user";

  return (
    <div
      style={{
        ...styles.row,
        flexDirection: isUser ? "row-reverse" : "row",
      }}
    >
      <div
        style={{
          ...styles.avatar,
          ...(isUser ? styles.userAvatar : styles.botAvatar),
        }}
      >
        {isUser ? "🙂" : "✨"}
      </div>
      <div style={isUser ? styles.bubbleUser : styles.bubbleBot}>{text}</div>
    </div>
  );
}