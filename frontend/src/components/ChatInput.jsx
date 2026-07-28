import { useState } from "react";

function ChatInput({ onSend }) {
  const [prompt, setPrompt] = useState("");

  const handleSend = () => {
    if (!prompt.trim()) return;

    onSend(prompt);
    setPrompt("");
  };

  return (
    <div className="border-t border-slate-700 p-5">

      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Type your request..."
        className="h-28 w-full resize-none rounded-xl bg-slate-900 p-4 text-white outline-none"
      />

      <div className="mt-4 flex justify-end">

        <button
          onClick={handleSend}
          className="rounded-xl bg-indigo-600 px-6 py-3 hover:bg-indigo-700"
        >
          Send →
        </button>

      </div>

    </div>
  );
}

export default ChatInput;