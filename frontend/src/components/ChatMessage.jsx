function ChatMessage({ sender, text }) {
  const isUser = sender === "user";

  return (
    <div className={`mb-6 flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-2xl rounded-2xl px-5 py-4 shadow-lg ${
          isUser
            ? "bg-indigo-600 text-white"
            : "border border-slate-700 bg-slate-800 text-slate-100"
        }`}
      >
        <div className="mb-2 text-xs font-semibold uppercase opacity-70">
          {isUser ? "You" : "SynapseOS"}
        </div>

        <div className="whitespace-pre-wrap">
          {text}
        </div>
      </div>
    </div>
  );
}

export default ChatMessage;