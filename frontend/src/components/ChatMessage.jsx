function ChatMessage({ sender, text }) {
  const isUser = sender === "user";

  return (
    <div
      className={`my-3 flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-xl rounded-2xl px-5 py-3 ${
          isUser
            ? "bg-indigo-600 text-white"
            : "bg-slate-800 text-slate-200"
        }`}
      >
        {text}
      </div>
    </div>
  );
}

export default ChatMessage;