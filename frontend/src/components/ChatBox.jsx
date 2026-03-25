import { useState } from "react";
import { sendQuery } from "../services/api";

function ChatBox({ onQuery }) {   // 🔥 accept onQuery
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Hi! I can help you analyze the Order to Cash process."
    }
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await sendQuery(input);

      console.log("CHAT RESPONSE:", res); // 🔥 debug

      const botMsg = {
        role: "bot",
        text: typeof res.answer === "string"
          ? res.answer
          : JSON.stringify(res.answer, null, 2),
      };

      setMessages((prev) => [...prev, botMsg]);

      // 🔥 IMPORTANT: send full response to App
      if (onQuery) {
        onQuery(res);
      }

    } catch (err) {
      console.error("Chat error:", err);

      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Error fetching response ❌" }
      ]);

      // reset highlight on error
      if (onQuery) {
        onQuery({ ids: [] });
      }
    }

    setLoading(false);
    setInput("");
  };

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      height: "100%",
      background: "#ffffff"
    }}>

      {/* HEADER */}
      <div style={{
        padding: "16px",
        borderBottom: "1px solid #e5e7eb"
      }}>
        <div style={{ fontWeight: "600", fontSize: "16px" }}>
          Chat with Graph
        </div>
        <div style={{ fontSize: "12px", color: "#6b7280" }}>
          Order-to-Cash
        </div>
      </div>

      {/* MESSAGES */}
      <div style={{
        flex: 1,
        overflowY: "auto",
        padding: "16px",
        display: "flex",
        flexDirection: "column",
        gap: "14px"
      }}>
        {messages.map((msg, i) => (
          <div key={i} style={{
            display: "flex",
            justifyContent: msg.role === "user" ? "flex-end" : "flex-start"
          }}>
            <div style={{
              background: msg.role === "user" ? "#2563eb" : "#f3f4f6",
              color: msg.role === "user" ? "white" : "#111827",
              padding: "10px 14px",
              borderRadius: "12px",
              maxWidth: "80%",
              fontSize: "14px",
              lineHeight: "1.4",
              whiteSpace: "pre-wrap"
            }}>
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{ fontSize: "12px", color: "#6b7280" }}>
            ⏳ Analyzing...
          </div>
        )}
      </div>

      {/* INPUT */}
      <div style={{
        borderTop: "1px solid #e5e7eb",
        padding: "12px",
        display: "flex",
        gap: "10px"
      }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Analyze anything"
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          style={{
            flex: 1,
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #d1d5db",
            outline: "none"
          }}
        />

        <button
          onClick={sendMessage}
          style={{
            padding: "10px 16px",
            background: "#2563eb",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer"
          }}
        >
          Send
        </button>
      </div>

    </div>
  );
}

export default ChatBox;