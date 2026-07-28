import { useState } from "react";

function ChatInput({ onSend }) {
  const [prompt, setPrompt] = useState("");

  const handleSend = () => {
    if (!prompt.trim()) return;

    onSend(prompt);
    setPrompt("");
  };

  return (
    <div className="border-t border-slate-800 bg-slate-950 p-6">

      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Ask SynapseOS to do anything..."
        className="h-32 w-full resize-none rounded-xl border border-slate-700 bg-slate-900 p-4 text-white outline-none focus:border-indigo-500"
      />

      <div className="mt-4 flex justify-end">

        <button
          onClick={handleSend}
          className="rounded-xl bg-indigo-600 px-8 py-3 font-semibold transition hover:bg-indigo-700"
        >
          Send →
        </button>

      </div>

    </div>
  );
}

export default ChatInput;