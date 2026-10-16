
import { useState } from "react";

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
    maxWidth: "100%",
    fontSize: "14.5px",
    lineHeight: 1.55,
    fontWeight: 600,
    whiteSpace: "pre-wrap",
    overflowWrap: "anywhere",
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
  },
  field: {
    display: "block",
    width: "100%",
    boxSizing: "border-box",
    padding: "10px",
    border: "1px solid #DCD3F0",
    borderRadius: "9px",
    font: "inherit",
    color: "#4A3F6B",
    background: "#fff",
  },
  label: {
    display: "block",
    margin: "12px 0 5px",
    fontSize: "12px",
    fontWeight: 800,
  },
  button: {
    padding: "9px 13px",
    borderRadius: "9px",
    border: "none",
    cursor: "pointer",
    fontWeight: 800,
  },
};

export default function ChatMessage({
  sender,
  text,
  emailDraft,
  onApprove,
  onSaveDraft,
  onCancel,
}) {
  const isUser = sender === "user";

  const [toEmail, setToEmail] = useState(emailDraft?.to_email || "");
  const [subject, setSubject] = useState(emailDraft?.subject || "");
  const [body, setBody] = useState(emailDraft?.body || "");

  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [draftStatus, setDraftStatus] = useState("pending");

  const handleCancel = async () => {
    if (busy || draftStatus !== "pending") return;

    setBusy(true);
    setError("");

    try {
      await onCancel(emailDraft.draft_id);
      setDraftStatus("cancelled");
    } catch (err) {
      setError(err.message || "Could not cancel this draft.");
    } finally {
      setBusy(false);
    }
  };

  const handleApprove = async () => {
    if (busy || draftStatus !== "pending") return;

    if (!toEmail.trim() || !subject.trim() || !body.trim()) {
      setError("Recipient, subject, and body are required.");
      return;
    }

    if (
      !window.confirm(
        `Send this email to ${toEmail.trim()}?`
      )
    ) {
      return;
    }

    setBusy(true);
    setError("");

    const approvedContent = {
      draft_id: emailDraft.draft_id,
      to_email: toEmail.trim(),
      subject: subject.trim(),
      message: body.trim(),
    };

    try {
      if (typeof onSaveDraft !== "function") {
        throw new Error(
          "Draft saving is not configured. Please try again later."
        );
      }

      // Save the exact edited content before sending.
      await onSaveDraft(approvedContent);

      // Only request sending after saving succeeds.
      await onApprove(approvedContent);

      setDraftStatus("sent");
    } catch (err) {
      setError(
        err.message || "Could not save or send the email."
      );
    } finally {
      setBusy(false);
    }
  };

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

      <div style={isUser ? styles.bubbleUser : styles.bubbleBot}>
        {text}

        {emailDraft && (
          <div
            style={{
              marginTop: "14px",
              padding: "14px",
              border: "1px solid #DCD3F0",
              borderRadius: "14px",
              background: "#F8F5FF",
              minWidth: 0,
            }}
          >
            <div style={{ fontSize: "16px", fontWeight: 900 }}>
              ✉️ Email preview
            </div>

            <div style={{ fontSize: "12px", marginTop: "4px" }}>
              Review the complete email before sending.
            </div>

            <label
              style={styles.label}
              htmlFor={`to-${emailDraft.draft_id}`}
            >
              To
            </label>
            <input
              id={`to-${emailDraft.draft_id}`}
              style={styles.field}
              type="email"
              value={toEmail}
              disabled={busy || draftStatus !== "pending"}
              onChange={(e) => setToEmail(e.target.value)}
            />

            <label
              style={styles.label}
              htmlFor={`subject-${emailDraft.draft_id}`}
            >
              Subject
            </label>
            <input
              id={`subject-${emailDraft.draft_id}`}
              style={styles.field}
              value={subject}
              disabled={busy || draftStatus !== "pending"}
              onChange={(e) => setSubject(e.target.value)}
            />

            <label
              style={styles.label}
              htmlFor={`body-${emailDraft.draft_id}`}
            >
              Email body
            </label>
            <textarea
              id={`body-${emailDraft.draft_id}`}
              style={{
                ...styles.field,
                minHeight: "160px",
                resize: "vertical",
              }}
              value={body}
              disabled={busy || draftStatus !== "pending"}
              onChange={(e) => setBody(e.target.value)}
            />

            {emailDraft.validation?.warnings?.map(
              (warning, index) => (
                <div
                  key={index}
                  style={{
                    marginTop: "8px",
                    color: "#8A5A00",
                    fontSize: "12px",
                  }}
                >
                  ⚠️ {warning}
                </div>
              )
            )}

            {error && (
              <div
                role="alert"
                style={{ color: "#B42318", marginTop: "10px" }}
              >
                {error}
              </div>
            )}

            {draftStatus === "pending" ? (
              <div
                style={{
                  display: "flex",
                  gap: "8px",
                  flexWrap: "wrap",
                  marginTop: "14px",
                }}
              >
                <button
                  type="button"
                  disabled={busy}
                  style={{
                    ...styles.button,
                    background: "#E7E1F5",
                    color: "#4A3F6B",
                  }}
                  onClick={handleCancel}
                >
                  {busy ? "Please wait..." : "Cancel draft"}
                </button>

                <button
                  type="button"
                  disabled={busy}
                  style={{
                    ...styles.button,
                    background: "#7564CB",
                    color: "#fff",
                  }}
                  onClick={handleApprove}
                >
                  {busy ? "Processing..." : "Approve & Send"}
                </button>
              </div>
            ) : (
              <div style={{ marginTop: "12px", fontWeight: 800 }}>
                {draftStatus === "sent"
                  ? "✅ Email sent"
                  : "Draft cancelled"}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
